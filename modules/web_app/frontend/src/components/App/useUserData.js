import { useState } from "react"

export default function useUserData() {
  const getUserData = () => {
    const userDataStr = sessionStorage.getItem("userData")
    return userDataStr && JSON.parse(userDataStr)
  }

  const [userData, setUserData] = useState(getUserData())

  const saveUserData = userData => {
    if (userData) sessionStorage.setItem("userData", JSON.stringify(userData))
    if (!userData) sessionStorage.removeItem("userData")
    setUserData(userData)
  }

  return {
    setUserData: saveUserData,
    userData
  }
}
