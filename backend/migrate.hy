(import sqlite3)

(eval-when-compile
 (import itertools [repeat]))

(setv conn-old (sqlite3.connect "instance/zvms.db")
      conn-new (sqlite3.connect "instance/zvms-new.db")
      cur-old (conn-old.cursor)
      cur-new (conn-new.cursor))

(with [f (open "sql.sql" :encoding "utf-8")]
      (cur-new.executescript (f.read)))

(defmacro direct-migrate [table #* fields]
  (let [[table-old table-new] (if (isinstance table hy.models.Symbol) 
                                #(table table)
                                table)
        [fields-old fields-new] (gfor i #(0 1)
                                      (.join ", " (gfor f fields
                                                        (if (isinstance f hy.models.Symbol) f (get f i)))))
        fields (lfor _ fields (hy.gensym))]
    `(do (cur-old.execute ~(.format "SELECT {} FROM {}" fields-old table-old))
         (for [[~@fields] (cur-old.fetchall)]
           (cur-new.execute ~(.format "INSERT INTO {}({}) VALUES({})"
                                      table-new
                                      fields-new
                                      (.join ", " (repeat "?" (len fields))))
                            #(~@fields))))))

(direct-migrate class id name)

(cur-old.execute "SELECT id, name, class, pwd, auth FROM user")

(defn mangle [name class]
  (+ name (if (> (% class 100) 10) "J" "") (str (% class 10))))

(for [[id name class pwd auth] (cur-old.fetchall)]
  (cur-old.execute "SELECT COUNT(*) FROM user WHERE name=?" #(name))
  (let [name (if (= (get (cur-old.fetchone) 0) 1)
               name
               (mangle name class))]
    (cur-new.execute "INSERT INTO user VALUES(?, ?, ?, ?, ?)"
                     #(id name class pwd auth))))

(direct-migrate notice id title content sender deadtime sendtime)

(direct-migrate volunteer id name description holder status time type reward)

(direct-migrate stu_vol [vol_id volunteer] [stu_id student] status thought reward reason)

(cur-old.execute "SELECT class_id, vol_id, max FROM class_vol")

(for [[class volunteer max] (cur-old.fetchall)]
  (cur-new.execute "INSERT INTO class_vol VALUES(?, ?, ?)"
                   #(volunteer class max)))

(cur-old.execute "SELECT stu_id, vol_id, hash, extension FROM picture")

(for [[student volunteer hash extension] (cur-old.fetchall)]
  (cur-new.execute "INSERT INTO picture VALUES(?, ?, ?)"
                   #(volunteer student (+ hash "." extension))))

(direct-migrate user_notice [user_id user] [notice_id notice])

(direct-migrate class_notice [class_id class] [notice_id notice])

(direct-migrate school_notice [notice_id notice])

(direct-migrate [report issue] id time [reporter author] content)

(conn-new.commit)
(conn-new.close)