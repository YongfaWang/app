//创建一个路由器，并暴露出去

//第一步 : 引入createRouter
import { createRouter, createWebHistory } from 'vue-router'

//引入一个一个可以能要呈现的组件

//第二步 : 创建路由器
const router = createRouter({
    history: createWebHistory(), //路由器的工作模式
    routes: [ //一个个的路由规则
        {
            path: '/home',
            component: () => import('@/views/Home/Home.vue'),
        }, {
            path: '/h5view',
            component: () => import('@/views/H5View/H5View.vue'),
        }, {
            path: '/orbits',
            component: () => import('@/views/Orbits/Orbits.vue'),
        }, {
            path: '/instrument',
            component: () => import('@/views/Instrument/Instrument.vue'),
        }, {
            path: '/glitchs',
            component: () => import('@/views/Glitchs/Glitchs.vue'),
        }, {
            path: '/gwresponse',
            component: () => import('@/views/GWResponse/GWResponse.vue'),
        }
    ]
})

//暴露出去
export default router
