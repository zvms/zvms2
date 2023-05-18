(import time [perf-counter])

(setv start (perf-counter))

(require zvms.util [case])

(import enum [IntEnum IntFlag]
        collections [defaultdict]
        itertools [chain]
        operator [itemgetter]
        typing [Optional]
        pprint [pprint]
        enum :as e
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
        (f.write (.join "" content)))
  (print (os.path.realpath file-name) "生成完成!"))

(defmacro for/join [sep it #* body]
  `(.join ~sep (gfor ~@it (.join "" (map str #(~@body))))))

(defn convert [ident src dst]
  (let [elems (map str.lower (case src
                               'snake (ident.split "_")
                               'upper-snake (ident.split "_")
                               'camel (chain #((.group (re.match r "^[a-z]*" ident))) (re.findall r "[A-Z][a-z]*" ident))
                               'pascal (re.findall r "[A-Z][a-z]*" ident)
                               'lisp (ident.split "-")
                               'url (ident.split "/")
                               'text (ident.split)))]
    (case dst
      'snake (.join "_" elems)
      'upper-snake (.join "_" (map str.upper elems))
      'camel (let [iter (iter elems)]
               (+ (next iter) (.join "" (map str.capitalize iter))))
      'pascal (.join "" (map str.capitalize elems))
      'lisp (.join "-" elems))))

(setv categs (sorted (gfor [k v] (res.Categ.__dict__.items)
                           :if (= (type v) res.Categ)
                           #(k v))
                     :key (itemgetter 1) :reverse True))

(defn auth->string [auth]
  (setv res [])
  (for [[k v] categs]
    :if (and (& auth v) (<= v auth))
    (res.append (convert k 'upper-snake 'pascal))
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
            (for/join "\n" [enum (res.__dict__.values)
                            :if (and (isinstance enum type) (issubclass enum e.Enum) (not-in enum #(IntEnum IntFlag)))
                            :setv map-this (get mapping enum.__name__)
                            :setv valid-cons (lfor [field value] (enum.__dict__.items)
                                                   :if (= (type value) enum)
                                                   #((convert field 'upper-snake 'pascal) value))] 
"export enum " enum.__name__ "{
" (for/join ",\n" [[field value] valid-cons]
"    " field " = " value)
"
}
export function get" enum.__name__ "Name(id: " enum.__name__ "): string {
    switch (id) {
" (for/join "" [[field _] valid-cons] 
"        case " enum.__name__ "." field ":
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
"export interface " struct.name (if (is struct.base None)
                                      "" 
                                      f" extends {struct.base.name}") " {
" (for/join ",\n" [[field value] (struct.fields.items) 
                   :if (isinstance value Processor)] 
            (+ "    " field (if struct.optional "?: " ": ") (value.render))) "
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

#_(for [api Api.apis]
  (pprint (vars api))
  (input))

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
  " (convert api.name 'lisp 'camel) "(" (if (not (has-params? api)) "" 
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