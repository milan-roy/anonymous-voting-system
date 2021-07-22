import React, { Component } from "react";
import logo from "../img/logo.jpg";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import Image from "react-bootstrap/Image";
import "../main.css";

class HomeRoute extends Component {
  state = {};
  render() {
    return (
      <Navbar bg="light" expand="lg">
        <Container>
          <Image src={logo} height="55" roundedCircle />
          <Navbar.Brand href="#home" className="brand_name">
            Votacion
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto" id="Navbar">
              <Nav.Item >
                <Nav.Link href="#home">Home</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                {" "}
                <Nav.Link href="#login">Login</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                {" "}
                <Nav.Link href="#signup">Signup</Nav.Link>
              </Nav.Item>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    );
  }
}

export default HomeRoute;
