import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:5000', // update if different
  withCredentials: true,
})

export default instance
