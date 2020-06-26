import React from "react";
import '../CSS/homeStyle.css';

function Home() {
    let name = 'Alfredo Mejia';
    let university = 'University of Texas at Dallas (UTD)';
    let major = 'Software Engineering';
    let gpa = '3.984 (4.0 Scale)';
    let graduation = 'May 2021';
    let city = 'Dallas';
    let email = 'a9.mejia@gmail.com';

    return (
        <div>
            <div className="picContainer"><img className="picture" src={require('../personalPic.jpg')}/><p>Hi there! I am Alfredo Mejia.</p></div>
            <div className="content">
                <span className="heading">Overview</span>
                <p className="quote">"It's fine to celebrate success but it is more important to heed the lessons of failure" - Bill Gates</p>
                <ul className="list">
                    <li>Name: <span className="value">{name}</span></li>
                    <li>University: <span className="value">{university}</span></li>
                    <li>Major: <span className="value">{major}</span></li>
                    <li>GPA: <span className="value">{gpa}</span></li>
                    <li>Graduation: <span className="value">{graduation}</span></li>
                    <li>City: <span className="value">{city}</span></li>
                    <li>Email: <span className="value">{email}</span></li>
                </ul>
                <img className="icon" src={require('../github-logo.png')}/>
                <img className="icon" src={require('../linkedIn-logo.png')}/>
            </div>
        </div>
    )

}

export default Home;
