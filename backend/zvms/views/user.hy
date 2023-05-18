(import jwt
        zvms.apilib *)

(require zvms.apilib *)

(defn generate-token [#**data]
  (import zvms [app])
  (jwt.encode data :key (:SECRET-KEY app.config)))

(defn read-token [token]
  (import zvms [app])
  (jwt.decode (token.encode) :key (:SECRET-KEY app.config) :algorithms "HS256"))