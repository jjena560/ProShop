import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import Rating from '../components/Rating'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { listProductDetails } from '../actions/productActions'


function ProductScreen({ match, history }) {
    // 1 is the default qty value
    const [qty, setQty] = useState(1)

    const dispatch = useDispatch()

    const productDetails = useSelector(state => state.productDetails)

    const { error, loading, product } = productDetails


    useEffect(() => {

        dispatch(listProductDetails(match.params.id))



    }, [dispatch, match])


    // const [product, setProduct] = useState([]) // right now the product is an empty array and whatever we 

    // useEffect(() => {

    //     async function fetchProduct() {
    //         const { data } = await axios.get(`/api/products/${match.params.id}`)
    //         setProduct(data)
    //     }

    //     fetchProduct()

    // }, [])


    const addToCartHandler = () => {

        history.push(`/cart/${match.params.id}?qty=${qty}`)
    }

    return (
        <div>
            <Link to="/" className='btn btn-light my-3'>Go Back</Link>

            {loading ? <Loader />
                : error ? <Message variant='danger'>{error}</Message>
                    : (
                        <Row>
                            <Col md={6}>
                                <Image src={product.image} alt={product.name} fluid />
                            </Col>


                            <Col md={3}>
                                <ListGroup variant='flush'>
                                    <ListGroup.Item>
                                        <h3>
                                            {product.name}
                                        </h3>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Rating value={product.rating} text={`${product.numReviews} reviews`} color={'f8e825'} />
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        Price: ${product.price}
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        Description : {product.description}
                                    </ListGroup.Item>
                                    <ListGroup.Item>

                                    </ListGroup.Item>
                                </ListGroup>
                            </Col>
                            <Col md={3}>
                                <Card>
                                    <ListGroup variant="flush">
                                        <ListGroup.Item>
                                            <Row>
                                                <Col>
                                                    Price:
                                    </Col>
                                                <Col>
                                                    <strong>${product.price}</strong>
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                        <ListGroup.Item>
                                            <Row>
                                                <Col>
                                                    Status:
                                    </Col>
                                                <Col>
                                                    {product.countInStock > 0 ? 'In Stock' : 'Out Of Stock'}
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>

                                        {product.countInStock > 0 && (
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col>Qty</Col>
                                                    <Col xs='auto' className='my-1'>
                                                        <Form.Control
                                                            as="select"
                                                            value={qty}
                                                            onChange={(e) => setQty(e.target.value)}
                                                        >
                                                            {

                                                                [...Array(product.countInStock).keys()].map((x) => (
                                                                    <option key={x + 1} value={x + 1}>
                                                                        {x + 1}
                                                                    </option>
                                                                ))
                                                            }

                                                        </Form.Control>
                                                    </Col>
                                                </Row>
                                            </ListGroup.Item>
                                        )}

                                        <ListGroup.Item>
                                            <Button
                                                onClick={addToCartHandler}
                                                className="btn-block"
                                                disabled={product.countInStock == 0}
                                                type='button'>Add To Cart</Button>
                                        </ListGroup.Item>
                                        <ListGroup.Item>
                                            <Button id='jp' className="coll btn-block" disabled={product.countInStock == 0} type='button'>Buy Now</Button>
                                        </ListGroup.Item>
                                    </ListGroup>

                                </Card>
                            </Col>
                        </Row>
                    )
            }


        </div >
    )
}

export default ProductScreen
