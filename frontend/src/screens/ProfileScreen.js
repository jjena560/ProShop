import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import Rating from '../components/Rating'
import Loader from '../components/Loader'
import Message from '../components/Message'

import { getUserDetails } from '../actions/userActions'

function ProfileScreen({ history, location }) {
    return (
        <Row>
            <Col md={3}>
                <h2>User Profile</h2>
            </Col>
            <Col md={9}>
                <h2>My Orders</h2>
            </Col>

        </Row>
    )
}

export default ProfileScreen
