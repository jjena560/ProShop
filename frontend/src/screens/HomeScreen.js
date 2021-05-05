import React, { useState, useEffect } from 'react'
// useDispatch to fire off the listProduct ACTION, useSelector let's us select a certain part of our state
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col } from 'react-bootstrap'
import Product from '../components/Product'
import axios from 'axios'

import { listProducts } from '../actions/productActions'

function HomeScreen() {
    const dispatch = useDispatch()
    //  for this read store.js
    const productList = useSelector(state => state.productList)
    const { error, loading, products } = productList
    

    console.log(productList)
    // {
    // useState ---- state is products and setproducts is used to update the products
    // const [products, setProducts] = useState([]) // right now the product is an empty array and whatever we put in this will be its actual value.
    // we need to make an api call and use the setProducts value to update the state of products
    // useEffect is triggered every time a component loads or the state value is updated
    //  }

    useEffect(() => {

        dispatch(listProducts())

        // {
        // we'll use axios to make the call, load in data and to make the updates
        // This is moved to productActions.js
        // async function fetchProducts() {
        //     const { data } = await axios.get('/api/products/') // axios returns a promise/respone
        //     setProducts(data) // now the state is what the response was 
        // }
        // fetchProducts()
        // }



    }, [dispatch])




    return (
        <div>
            <h1>Latest Products</h1>
            <Row>
                {/*  mapping every single product arrow function     */}
                {products.map(product => (
                    <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                        <Product product={product} />
                    </Col>
                ))}

            </Row>
        </div>
    )
}

export default HomeScreen
