import { createContext } from "react"

export const AuthContext = createContext({
    isLoggedIn: localStorage['user'] ? true : false,
    taken: null,
    getUser: () => { },
    login: () => { },
    logout: () => { }
})
