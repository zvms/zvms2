import Axios from "axios";
import { useInfoStore } from "../stores";

export function initAxios() {
  Axios.defaults.baseURL = "http://10.49.23.47:0";
  //Axios携带cookie
  Axios.defaults.withCredentials = true;
  //post设定，自动序列化表单的json数据
  Axios.defaults.headers.post["Content-Type"] =
    "application/x-www-form-urlencoded";
  //如果要把表单数据转化为url格式就去掉注释
  // Axios.defaults.transformRequest = [function (data){
  //     data = qs.stringify(data);
  //     return data;
  // }]

  const infoStore = useInfoStore();

  Axios.interceptors.request.use(
    (config) => {
      config.params = {
        ...config.params,
      };
      config.headers = config.headers ?? {};
      config.headers.Authorization = infoStore.token || "";
      return config;
    },
    (error) => Promise.reject(error)
  );
}
