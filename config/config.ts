const zvmsConfig = {
    paths: {
        f: {
            fApi: "/web/src/apis/fApi/",
            users: "/web/src/apis/users/",
            types: "/web/src/apis/types/"
        },
        b: {
            views: "/backend/zvms/views/",
            impls: "/backend/zvms/impls/",
            res: "/backend/zvms/res/",
            users: "/backend/zvms/res/users/",
            types: "/backend/zvms/res/types/"
        },
        backup: "/.backup/"
    }
}

export default zvmsConfig;