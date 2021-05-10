import Header from './components/Header'
import Footer from './components/Footer'
import { Container } from 'react-bootstrap'
import HomeScreen from './screens/HomeScreen'
import ProductScreen from './screens/ProductScreen'
import CartScreen from './screens/CartScreen'
import LoginScreen from './screens/LoginScreen'
import RegisterScreen from './screens/RegisterScreen'
import ProfileScreen from './screens/ProfileScreen'
import ShippingScreen from './screens/ShippingScreen'
import PaymentScreen from './screens/PaymentScreen'
import PlaceOrderScreen from './screens/PlaceOrderScreen'

import { BrowserRouter as Router, Route } from 'react-router-dom'
function App() {
  return (
    <Router>
      <Header />
      {/* py is for padding because we're using bootstrap */}
      <main className='py-3'>
        <Container>
          < Route path='/' component={HomeScreen} exact />
          < Route path='/login' component={LoginScreen} />
          < Route path='/register' component={RegisterScreen} />
          < Route path='/profile' component={ProfileScreen} />
          < Route path='/payment' component={PaymentScreen} />
          <Route path='/shipping' component={ShippingScreen} />
          <Route path='/placeorder' component={PlaceOrderScreen} />
          < Route path='/product/:id' component={ProductScreen} />
          {/* the question mark makes it an optiaonal parameter */}
          <Route path='/cart/:id?' component={CartScreen} />
        </Container>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
