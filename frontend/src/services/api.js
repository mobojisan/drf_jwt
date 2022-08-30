import axios from "axios";
import store from "@/store";

const api = axios.create({
  baseURL: process.env.VUE_APP_ROOT_API,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest"
  }
});

// sync
api.interceptors.request.use(
  config => {
    store.dispatch("message/clearMessages");
    const token = localStorage.getItem("access");
    if (token) {
      config.headers.Authorization = "JWT " + token;
      return config;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.log("error.response=", error.response);
    const status = error.response ? error.response.status : 500;

    let message;
    if (status === 400) {
      const messages = [].concat.apply([], Object.values(error.response.data));
      store.dispatch("message/setWarningMessages", { messages: messages });
    } else if (status === 401) {
      const token = localStorage.getItem("access");
      if (token != null) {
        message = "Out of date";
      } else {
        message = "Auth error";
      }
      store.dispatch("auth/logout");
      store.dispatch("message/setErrorMessage", { message: message });
    } else if (status === 403) {
      // 権限エラー
      message = "Perm error";
      store.dispatch("message/setErrorMessage", { message: message });
    } else {
      // その他のエラー
      message = "Unexpected error";
      store.dispatch("message/setErrorMessage", { message: message });
    }
    return Promise.reject(error);
  }
);

export default api;
