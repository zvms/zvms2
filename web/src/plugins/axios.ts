import { useInfoStore } from "@/stores";
import Axios from "axios";
// import NProgress from "nprogress";
import "nprogress/nprogress.css";

const axios = Axios.create({
  baseURL: "http://172.31.2.3:1145",
  withCredentials: true,
  headers: {
    "Content-type": "application/json",
  },
  timeout: 6000,
});

axios.interceptors.request.use(
  (config) => {
    const infoStore = useInfoStore();

    config.params = {
      ...config.params,
    };
    config.headers = config.headers ?? {};
    config.headers.Authorization = infoStore.token || "";
    return config;
  },
  (error) => Promise.reject(error)
);

export default axios;

// request.interceptors.request.use(
//   (config) => {
//     NProgress.start();
//     return config;
//   },
//   (error) => {
//     NProgress.done();
//     return Promise.reject(error);
//   }
// );

// request.interceptors.response.use(
//   (response) => {
//     NProgress.done();
//     return response;
//   },
//   (error) => {
//     NProgress.done();
//     return Promise.reject(error);
//   }
// );
