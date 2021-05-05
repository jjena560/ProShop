import Header from './components/Header'
import Footer from './components/Footer'
import { Container } from 'react-bootstrap'
import HomeScreen from './screens/HomeScreen'
import ProductScreen from './screens/ProductScreen'
import CartScreen from './screens/CartScreen'

import { BrowserRouter as Router, Route } from 'react-router-dom'
function App() {
  return (
    <Router>
      <Header />
      {/* py is for padding because we're using bootstrap */}
      <main className='py-3'>
        <Container>
          < Route path='/' component={HomeScreen} exact />
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
