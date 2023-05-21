(import time [perf-counter])

(setv start (perf-counter))

(require zvms.util [case])

(import enum [IntEnum IntFlag]
        collections [defaultdict]
        itertools [chain]
        operator [itemgetter]
        typing [Optional]
        pprint [pprint]
        json
        sys
        re
        os
        yaml
        zvms.res :as res
        zvms.views
        zvms.typing *
        zvms.apilib [Api])

(defn write-file [file-name #* content]
  (with [f (open file-name "w" :encoding "utf-8")]
        (f.write (.join "" (map str content))))
  (print (os.path.realpath file-name) "生成完成!"))

(defmacro for/join [sep it #* body]
  `(.join ~sep (gfor ~@it (.join "" (map str #(~@body))))))

(setv categs (sorted (gfor [k v] (res.Categ.__dict__.items)
                           :if (= (type v) res.Categ)
                           #(k v))
                     :key (itemgetter 1) :reverse True))

(defn auth->string [auth]
  (setv res [])
  (for [[k v] categs]
    :if (and (& auth v) (<= v auth))
    (res.append k)
    (&= auth (bnot v))
    (when (= auth 0)
      (return res))))

(with [config-file (open "genconfig.yaml" :encoding "utf-8")]
      (setv config (yaml.full-load (config-file.read))))

(with [mapping-file (open (get config "enums-mapping") :encoding "utf-8")
       template-file (open (get config "apis-template") :encoding "utf-8")]
      (setv mapping (yaml.full-load (mapping-file.read))
            template (template-file.read)))

(write-file (get config "enums")
            "export var PORT = " res.PORT ";\n\n"
            (for/join "\n" [[name enum] (Api.enums.items)
                            :setv map-this (get mapping name)]
"export enum " name "{
" (for/join ",\n" [[field value] (enum.items)]
"    " field " = " value)
"
}
export function get" name "Name(id: " name "): string {
    switch (id) {
" (for/join "" [[field _] (enum.items)] 
"        case " name "." field ":
            return \"" (get map-this field) "\";
")
"        default:
             throw new Error(\"Invalid enum value\");
    }
}
"))

(write-file (get config "structs") 
"import * as enums from \"./enums\";

" (for/join "" [struct (Api.structs.values)] 
              (+ 
               (if (is-not struct.doc None) 
                 f"/* {struct.doc} */\n" 
                 "")
"export interface " struct.name " {
" (for/join ",\n" [[field value] (struct.fields.items) 
                   :if (isinstance value Processor)] 
            (+ "    " field ": " (value.render))) "
}
    
")))

(setv rule-methods-block (re.compile (str.format r"{}.+{}"
                                                 (get config "methods-flag" "start") (get config "methods-flag" "end")) re.S))

(setv rule-to-url (re.compile r"(.+?)\<(?:int:)?(.+?)\>")
      rule-to-url-sub r"\1${\2}"
      Object.module "structs.")

(defn gen-url [api]
  (rule-to-url.sub rule-to-url-sub api.rule))

(defn has-params? [api]
  (or api.url-params (not (isinstance api.params Any))))

(write-file (get config "apis")
            (rule-methods-block.sub (+ (for/join "" [api Api.apis]
                                                 "
  /**" (if (is api.doc None) "" (+ "
   * ## " api.doc)) "
   * ### [" api.method "] " api.rule "
   * #### 权限: " (.join " | " (auth->string api.auth)) (if (not (has-params? api)) "" 
                                                          (+ "\n" (for/join "\n" [name (chain api.url-params (api.params.as-params))] 
"   * @param " name))) "
   */
  " api.name "(" (if (not (has-params? api)) "" 
                                                      (+ "\n" (for/join ",\n" [[name type] (chain (api.url-params.items) (.items (api.params.as-params)))] 
 "    " name ": " type) "
  ")) "): ForegroundApiRunner<" (api.returns.render) "> {
    return createForegroundApiRunner(" (if (not (has-params? api))
                                         (+ "this, \"" api.method "\", `" (gen-url api) "`")
                                         (+ "
      this,
      \"" api.method "\",
      `" (gen-url api) (let [params (api.params.as-params)
                             args (if (isinstance api.params Any) ""
                                      (for/join ",\n" [arg (api.params.as-params)]
"        " arg))] (if (= api.method "POST") 
                                                                    (if params (+ "`, {
" args "
      }") "`,
      {}")
                                                                    (if params (+ "?` + toURLSearchParams(
" args "
      )") "`"))) "
    ")) ");
  }
") "

") template))

(write-file (get config "doc")
            (let [modules (defaultdict list)]
              (for [api Api.apis]
                (.append (get modules api.func.__module__) api)) (+
                                                                  "# 镇海中学义工管理系统API文档

" (for/join "" [[i [module apis]] (enumerate (modules.items) 1)]
            "## " i "." module "

### **" (.__dict__.get (get sys.modules module) "SUMMARY" "...") "**
" (for/join "" [[j api] (enumerate apis 1)] "
#### " i "." j " " api.name "

[" api.method "] " api.rule "  
**" (or api.doc "...") "**  

参数:
```json
" (json.dumps (api.params.jsonify) :indent 4) "
```
返回:
```json
" (json.dumps (api.returns.jsonify) :indent 4) "
```
")))))

(print (- (perf-counter) start))