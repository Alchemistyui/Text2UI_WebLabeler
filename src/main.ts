/*
 * @Author: Alchemistyui
 * @Date: 2023-02-20
 * @LastEditTime: 2023-02-20
 * @FilePath: /Text2UI_WebLabeler/src/main.ts
 * @Description: 
 * 
 * Copyright (c) 2023, All Rights Reserved. 
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)

app.mount('#app')
