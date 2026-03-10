import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor để thêm token
api.interceptors.request.use(
    (config) => {
        const customer = localStorage.getItem('customer')
        if (customer) {
            const { id } = JSON.parse(customer)
            config.headers['X-Customer-ID'] = id
        }
        return config
    },
    (error) => Promise.reject(error)
)

// Response interceptor để xử lý lỗi
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('customer')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default api
