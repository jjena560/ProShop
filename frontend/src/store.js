import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { productListReducer } from './reducers/productReducers'

const reducer = combineReducers({
    // this is one reducer below and we select the reducer by using useSelector
    productList: productListReducer,
})

const intitalState = {}
const middleWare = [thunk]

const store = createStore(reducer, intitalState, composeWithDevTools(applyMiddleware(...middleWare)))

export default store