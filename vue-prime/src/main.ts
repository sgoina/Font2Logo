import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import Primevue from 'primevue/config'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import Sidebar from 'primevue/sidebar'
import Button from 'primevue/button'
import Toolbar from 'primevue/toolbar'
import Slider from 'primevue/slider'
import ScrollPanel from 'primevue/scrollpanel'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Carousel from 'primevue/carousel'
import Stepper from 'primevue/stepper'
import StepperPanel from 'primevue/stepperpanel'
import Timeline from 'primevue/timeline'
import Splitter from 'primevue/splitter'
import SplitterPanel from 'primevue/splitterpanel'
import Galleria from 'primevue/galleria'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import ProgressBar from 'primevue/progressbar'
import ToggleButton from 'primevue/togglebutton'
import Ripple from 'primevue/ripple'
import ToastService from 'primevue/toastservice'
import Toast from 'primevue/toast'
import FileUpload from 'primevue/fileupload'
import Image from 'primevue/image'
import Skeleton from 'primevue/skeleton'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Primevue, { ripple: true })
app.use(ToastService)
app.directive('ripple', Ripple)

app.component('Sidebar', Sidebar)
app.component('Button', Button)
app.component('Toolbar', Toolbar)
app.component('Slider', Slider)
app.component('ScrollPanel', ScrollPanel)
app.component('TabView', TabView)
app.component('TabPanel', TabPanel)
app.component('Carousel', Carousel)
app.component('Stepper', Stepper)
app.component('StepperPanel', StepperPanel)
app.component('Timeline', Timeline)
app.component('Splitter', Splitter)
app.component('SplitterPanel', SplitterPanel)
app.component('Galleria', Galleria)
app.component('IconField', IconField)
app.component('InputIcon', InputIcon)
app.component('InputText', InputText)
app.component('Dropdown', Dropdown)
app.component('ProgressBar', ProgressBar)
app.component('ToggleButton', ToggleButton)
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)
app.component('Image', Image)
app.component('Skeleton', Skeleton)

app.mount('#app')
