import React from "react";
import {Switch, Route} from 'react-router-dom';
import Home from "./Home";
import Skills from "./Skills";
import Experience from "./Experience";
import Projects from "./Projects";
import Hackathons from "./Hackathons";
import Classes from "./Classes";
import LeadershipAwards from "./LeadershipAwards";
import AboutMe from "./AboutMe";


function Router() {
    return (
        <main>
            <Switch>
                <Route exact path='/' component={Home}/>
                <Route path='/Skills' component={Skills}/>
                <Route path='/Experience' component={Experience}/>
                <Route path='/Projects' component={Projects}/>
                <Route path='/Hackathons' component={Hackathons}/>
                <Route path='/Classes' component={Classes}/>
                <Route path='/LeadershipAwards' component={LeadershipAwards}/>
                <Route path='/AboutMe' component={AboutMe}/>
            </Switch>
        </main>
    )
}

export default Router;
