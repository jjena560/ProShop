import {
    CART_ADD_ITEM,
    CART_REMOVE_ITEM
} from '../constants/cartConstants'
import axios from 'axios'


export const addToCart = (id, qty) => async (dispatch, getState) => {
    const { data } = await axios.get(`/api/products/${id}`)
    console.log(data)

    dispatch({
        type: CART_ADD_ITEM,
        payload: {
            //  product is the id
            product: data._id,
            name: data.name,
            image: data.image,
            price: data.price,
            countInStock: data.countInStock,
            qty
        }
    })



    // this will take key value pair both in string format only
    // then once we want to get this data then we can parse it and turn it back it into an object
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))


}

export const removeFromCart = (id) => async (dispatch, getState) => {
    dispatch({
        type: CART_REMOVE_ITEM,
        payload: id,
    })
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}