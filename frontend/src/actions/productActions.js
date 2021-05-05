import {
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL
} from '../constants/productConstants'

import axios from 'axios'

import { productListReducer } from '../reducers/productReducers'

// redux thunk allows to make function inside a function


export const listProducts = () => async (dispatch) => {

    console.log("hello")
    try {
        dispatch({ type: 'PRODUCT_LIST_REQUEST' })

        // rather than the homescreen now the action will make the API call
        const { data } = await axios.get('http://127.0.0.1:8000/api/products/')

        dispatch({
            type: 'PRODUCT_LIST_SUCCESS',
            payload: data
        })

    } catch (error) {
        dispatch({
            type: 'PRODUCT_LIST_FAIL',
            payload: error.message
        })


    }
}