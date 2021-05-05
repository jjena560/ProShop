import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { productListReducer, productDetailsReducer } from './reducers/productReducers'

import { cartReducer } from './reducers/cartReducers'


const reducer = combineReducers({
    // the keys will be the states
    // this is one reducer below and we select the reducer by using useSelector
    productList: productListReducer, // this triggers the first call of reducer
    productDetails: productDetailsReducer,
    cart: cartReducer
})

// gettig the data from localStorage with key==='cartitems but first checking if it actually exists
const cartItemsFromStorage = localStorage.getItem('cartItems') ?
    JSON.parse(localStorage.getItem('cartItems')) : []


const intitalState = {
    // state-key-value
    cart: { cartItems: cartItemsFromStorage }
}

const middleWare = [thunk]

const store = createStore(reducer, intitalState, composeWithDevTools(applyMiddleware(...middleWare)))

export default store