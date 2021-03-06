import 'font-awesome/css/font-awesome.min.css'
import React from "react"
import { BrowserRouter, Route, Switch } from "react-router-dom"
import Footer from '../../shared/components/Footer/Footer'
import NavigationBar from "../../shared/components/navigation-bar/navigation-bar"
import Dashboard from "../Dashboard/Dashboard"
import Login from "../Login/Login"
import Preferences from "../Preferences/Preferences"
import SimilarityReport from "../Similarity-Report/Similarity-Report"
import "./App.css"
import useUserData from './useUserData'

function App() {
  const { userData, setUserData } = useUserData()
  const token = userData && userData.accessToken

  return (
    <BrowserRouter>
      <div className="App">
        <NavigationBar setUserData={setUserData} isLoggedIn={token ? true : false} />
        <div className="page-content">
          <Switch>
            <Route exact path="/" component={() => !token ? <Login setUserData={setUserData} /> : <Dashboard />} />
            <Route exact path="/sign-in" component={() => <Login setUserData={setUserData} />} />
            <Route exact path="/dashboard" component={Dashboard} />
            <Route exact path="/preferences" component={Preferences} />
            <Route exact path="/similarity-reports" component={() => <SimilarityReport userData={userData} />} />
            <Route exact path="/similarity-reports/:id" component={() => <SimilarityReport userData={userData} />} />
          </Switch>
        </div>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
