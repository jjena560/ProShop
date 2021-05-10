import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { productListReducer, productDetailsReducer } from './reducers/productReducers'

import { cartReducer } from './reducers/cartReducers'
import { userLoginReducer } from './reducers/userReducers'
import { userRegisterReducer, userDetailsReducer, userUpdateProfileReducer } from './reducers/userReducers'


const reducer = combineReducers({
    // the keys will be the states
    // this is one reducer below and we select the reducer by using useSelector
    productList: productListReducer, // this triggers the first call of reducer
    productDetails: productDetailsReducer,
    cart: cartReducer,
    userLogin: userLoginReducer,
    userRegister: userRegisterReducer,
    userDetails: userDetailsReducer,
    userUpdateProfile: userUpdateProfileReducer,
})

// gettig the data from localStorage with key==='cartitems but first checking if it actually exists
const cartItemsFromStorage = localStorage.getItem('cartItems') ?
    JSON.parse(localStorage.getItem('cartItems')) : []

const userInfoFromStorage = localStorage.getItem('userInfo') ?
    JSON.parse(localStorage.getItem('userInfo')) : null


const shippingInfoFromStorage = localStorage.getItem('shippingAddress') ?
    JSON.parse(localStorage.getItem('shippingAddress')) : {}

const intitalState = {
    // state-key-value
    cart: {
        cartItems: cartItemsFromStorage,
        shippingAddress: shippingInfoFromStorage
    },
    userLogin: { userInfo: userInfoFromStorage }
}

const middleWare = [thunk]

const store = createStore(reducer, intitalState, composeWithDevTools(applyMiddleware(...middleWare)))

export default store