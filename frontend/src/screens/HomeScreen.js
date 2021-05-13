import React, { useState, useEffect } from 'react'
// useDispatch to fire off the listProduct ACTION, useSelector let's us select a certain part of our state
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { Row, Col } from 'react-bootstrap'
import Product from '../components/Product'



import { listProducts } from '../actions/productActions'

function HomeScreen({ history }) {
    const dispatch = useDispatch()
    //  for this read store.js
    //  from homescreen we're triggering listProduct ACTION
    const productList = useSelector(state => state.productList)

    const { error, loading, products } = productList

    // so now anytime the keyword changes its gonna reload as it is a dependecy now in the useffect
    let keyword = history.location.search


    // {
    // useState ---- state is products and setproducts is used to update the products
    // const [products, setProducts] = useState([]) // right now the product is an empty array and whatever we put in this will be its actual value.
    // we need to make an api call and use the setProducts value to update the state of products
    // useEffect is triggered every time a component loads or the state value is updated
    //  }
    console.log(keyword)
    useEffect(() => {

        dispatch(listProducts(keyword))


        // {
        // we'll use axios to make the call, load in data and to make the updates
        // This is moved to productActions.js
        // async function fetchProducts() {
        //     const { data } = await axios.get('/api/products/') // axios returns a promise/respone
        //     setProducts(data) // now the state is what the response was 
        // }
        // fetchProducts()
        // }



    }, [dispatch, keyword])


    return (
        <div>
            <h1>Latest Products</h1>
            {loading ? <Loader />
                : error ? <Message>{error}</Message>
                    :
                    <Row>
                        {/*  mapping every single product arrow function     */}
                        {products.map(product => (
                            <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                                {/* this product component will structure all the products as 'Product.js */}
                                <Product product={product} />
                            </Col>
                        ))}

                    </Row>
            }

        </div >
    )
}

export default HomeScreen
