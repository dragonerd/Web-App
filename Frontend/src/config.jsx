import axios from "axios";

export const dbConnect = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 1000,
  headers: {
    "X-Custom-Header": "foobar",
    "X-CSRF-TOKEN": localStorage.getItem("csrf_token"),
  },
});

export default dbConnect;
