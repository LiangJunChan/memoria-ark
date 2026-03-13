import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vant UI
import { 
  Button, 
  Cell, 
  CellGroup, 
  Field, 
  Form, 
  NavBar, 
  Tabbar, 
  TabbarItem,
  Icon,
  Toast,
  Dialog,
  Loading,
  Uploader,
  Card,
  Tag,
  Grid,
  GridItem,
  Image,
  List,
  PullRefresh,
  Popup,
  Swipe,
  SwipeItem,
  Stepper,
  RadioGroup,
  Radio,
  Checkbox,
  CheckboxGroup,
  Slider
} from 'vant'

// Vant styles
import 'vant/lib/index.css'

const app = createApp(App)

// Use Pinia
app.use(createPinia())

// Use Router
app.use(router)

// Register Vant components
app.use(Button)
app.use(Cell)
app.use(CellGroup)
app.use(Field)
app.use(Form)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Icon)
app.use(Toast)
app.use(Dialog)
app.use(Loading)
app.use(Uploader)
app.use(Card)
app.use(Tag)
app.use(Grid)
app.use(GridItem)
app.use(Image)
app.use(List)
app.use(PullRefresh)
app.use(Popup)
app.use(Swipe)
app.use(SwipeItem)
app.use(Stepper)
app.use(RadioGroup)
app.use(Radio)
app.use(Checkbox)
app.use(CheckboxGroup)
app.use(Slider)

app.mount('#app')
