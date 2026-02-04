import axios from "axios";


const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});


export default api;


// Upload
export const uploadFile = async (file: File) => {

  const form = new FormData();
  form.append("file", file);

  return api.post("/upload", form);
};


// Ask
export const askQuestion = async (q: string) => {

  return api.post("/ask", {
    question: q
  });
};
