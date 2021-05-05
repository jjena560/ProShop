import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { Row, Col, Buttons, Card, Image, Form, ListGroup, Button } from 'react-bootstrap'
import { Message } from '../components/Message'
import { addToCart, removeFromCart } from '../actions/cartAction'
import { useLocation } from 'react-router-dom'

function CartScreen({ match, location, history }) {
    const productId = match.params.id
    // this is checking if the the product is already in the cart or not and it returns a string like = '?qty=7'
    //  so we want to get the last number only that is why we're splitting it and taking the number only
    const qty = location.search ? Number(location.search.split('=')[1]) : 1

    const dispatch = useDispatch()

    const cart = useSelector(state => state.cart)
    const { cartItems } = cart
    // console.log('cartItems:', cartItems)

    useEffect(() => {
        if (productId) {
            dispatch(addToCart(productId, qty))
        }
    }, [dispatch, productId, qty])

    const removeFromCartHandler = (id) => {
        dispatch(removeFromCart(id))
    }

    const checkOutHandler = () => {
        history.push('/login?redirect=shipping')
    }


    return (
        <Row>
            <Col md={8}>
                <h1>Shopping Cart</h1>
                {cartItems.length == 0 ? (
                    <Message variant='info'>Your cart is empty <Link to='/'>Go Back</Link></Message>
                ) : (
                    <ListGroup variant='flush'>
                        {cartItems.map(item => (
                            <ListGroup.Item key={item.product}>
                                <Row>
                                    <Col md={2}>
                                        <Image src={item.image} alt={item.name} fluid rounded />
                                    </Col>
                                    <Col md={3}>
                                        <Link to={`/product/${item.product}`}>{item.name}</Link>
                                    </Col>
                                    <Col md={2}>
                                        ${item.price}
                                    </Col>
                                    <Col md={3}>
                                        <Form.Control
                                            as="select"
                                            value={item.qty}
                                            // item.product is the id itself
                                            onChange={(e) => dispatch(addToCart(item.product, Number(e.target.value)))}>
                                            {

                                                [...Array(item.countInStock).keys()].map((x) => (
                                                    <option key={x + 1} value={x + 1}>
                                                        {x + 1}
                                                    </option>
                                                ))
                                            }

                                        </Form.Control>
                                    </Col>
                                    <Col md={1}>
                                        <Button type='button'
                                            variant='light'
                                            onClick={() => removeFromCartHandler(item.product)}>
                                            <i className='fa fa-trash'></i>
                                        </Button>
                                    </Col>
                                </Row>
                            </ListGroup.Item>
                        ))}

                    </ListGroup>
                )}
            </Col>
            <Col md={4}>
                <Card>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            {/* {/* LOOK THIS UP .reduce *  it takes two para(accumulator and the item we're looping through/} */}
                            <h2>SubTotal:({cartItems.reduce((acc, item) => acc + item.qty, 0)}) items</h2>
                            {/* to fixed is to constraint to 2 decimal places  */}
                            ${cartItems.reduce((acc, item) => acc + item.qty * item.price, 0).toFixed(2)}
                        </ListGroup.Item>
                    </ListGroup>
                    <ListGroup>
                        <Button
                            type='button'
                            className='btn btn-block'
                            disabled={cartItems.length === 0}
                            onClick={checkOutHandler}> Proceed to Checkout</Button>
                    </ListGroup>
                </Card>
            </Col>
        </Row >

    )
}

export default CartScreen
