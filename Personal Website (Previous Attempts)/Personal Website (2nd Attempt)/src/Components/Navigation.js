import React, {useState} from 'react';
import '../CSS/navigationStyle.css';
import {Link} from "react-router-dom";

function Navigation() {

    const [status, setStatus] = useState("Home");

    return (
        <header>
            <nav className="navigation">
                <ul className="navigationMenu">
                    <li><Link to='/' className="navItem activePage" id="Home" onClick={() => changeClassName("Home")}>Home</Link></li>
                    <li><Link to='/Skills' className="navItem" id="Skills" onClick={() => changeClassName("Skills")}>Skills</Link></li>
                    <li><Link to='/Experience' className="navItem" id="Experience" onClick={() => changeClassName("Experience")}>Experience</Link></li>
                    <li><Link to='/Projects' className="navItem" id="Projects" onClick={() => changeClassName("Projects")}>Projects</Link></li>
                    <li><Link to='/Hackathons' className="navItem" id="Hackathons" onClick={() => changeClassName("Hackathons")}>Hackathons</Link></li>
                    <li><Link to='/Classes' className="navItem" id="Classes" onClick={() => changeClassName("Classes")}>Classes</Link></li>
                    <li><Link to='/LeadershipAwards' className="navItem" id="Leadership & Awards" onClick={() => changeClassName("Leadership & Awards")}>Leadership & Awards</Link></li>
                    <li><Link to='/AboutMe' className="navItem" id="About Me" onClick={() => changeClassName("About Me")}>About Me</Link></li>
                </ul>
            </nav>

            <nav className="sideBarNav">
                <div id="mySidenav" className="sidenav">
                    <a href="javascript:void(0)" className="closebtn" onClick={() => (closeNav(""))}>&times;</a>
                    <Link to='/' onClick={() => (closeNav("Home"))}>Home</Link>
                    <Link to='/Experience' onClick={() => (closeNav("Experience"))}>Experience</Link>
                    <Link to='/Projects' onClick={() => (closeNav("Projects"))}>Projects</Link>
                    <Link to='/Hackathons' onClick={() => (closeNav("Hackathons"))}>Hackathons</Link>
                    <Link to='/Classes' onClick={() => (closeNav("Classes"))}>Classes</Link>
                    <Link to='/LeadershipAwards' onClick={() => (closeNav("Leadership & Awards"))}>Leadership & Awards</Link>
                    <Link to='/AboutMe' onClick={() => (closeNav("About Me"))}>About Me</Link>
                </div>
                <span onClick={openNav} className="icon">&#9776; {status}</span>
            </nav>
        </header>
    )
    function closeNav(x1) {
        if(x1 !== "") {
            setStatus(x1);
            changeClassName(x1)
        }
        document.getElementById("mySidenav").style.width = "0";
    }
    function openNav() {
        document.getElementById("mySidenav").style.width = "250px";
    }
    function changeClassName(x){
        if(x !== "Home")
        {
            let x1 = document.getElementById("Home");
            x1.className = "navItem";
        }
        if(x !== "Skills")
        {
            let x1 = document.getElementById("Skills");
            x1.className = "navItem";
        }
        if(x !== "Experience")
        {
            let x1 = document.getElementById("Experience");
            x1.className = "navItem";
        }
        if(x !== "Projects")
        {
            let x1 = document.getElementById("Projects");
            x1.className = "navItem";
        }
        if(x !== "Hackathons")
        {
            let x1 = document.getElementById("Hackathons");
            x1.className = "navItem";
        }
        if(x !== "Classes")
        {
            let x1 = document.getElementById("Classes");
            x1.className = "navItem";
        }
        if(x !== "Leadership & Awards")
        {
            let x1 = document.getElementById("Leadership & Awards");
            x1.className = "navItem";
        }
        if(x !== "About Me")
        {
            let x1 = document.getElementById("About Me");
            x1.className = "navItem";
        }
        const x1 = document.getElementById(x);
        x1.className += " activePage";
        setStatus(x);
    }
}


export default Navigation;
