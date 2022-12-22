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
            users: "/backend/zvms/users/",
            types: "/backend/zvms/types/"
        },
        backup: "/.backup/"
    }
}

export default zvmsConfig;