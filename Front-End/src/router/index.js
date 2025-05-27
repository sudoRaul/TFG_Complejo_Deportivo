import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import UsersAdmin from '@/views/UsersAdmin.vue'
import FacilitiesView from '@/views/FacilitiesView.vue'
import IndividualFacility from '@/views/IndividualFacility.vue'
import CreateFacilities from '@/views/CreateFacilities.vue'
import Assistants from '@/views/Assistants.vue'
import Messages from '@/views/Messages.vue'
import Contact from '@/views/Contact.vue'
import MyProfile from '@/views/MyProfile.vue'
import PhysicalAnalysis from '@/views/PhysicalAnalysis.vue'
import Reserves from '@/views/Reserves.vue'
import InfoUsers from '@/views/InfoUsers.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
          {
            path: '/',
            name: 'home',
            component: HomeView,
          },
          {
            path: '/login',
            name: 'login',
            component: LoginView,
          },
          {
            path: "/user-panel",
            name: "user-panel",
            component: UsersAdmin,
          },
          {
            path: "/facilities",
            name: "facilities",
            component: FacilitiesView,
          },
          {
            path: '/facilities/:category',
            name: 'category',
            component: IndividualFacility, 
            props: true,  
          },
          {
            path: '/create-facility',
            name: 'create-facility',
            component: CreateFacilities,
          },
          {
            path: '/assistants',
            name: 'assistants',
            component: Assistants,
          },
          {
            path: '/messages',
            name: 'messages',
            component: Messages,
          },
          {
            path: '/contact',
            name: 'contact',
            component: Contact,
          },
          {
            path: '/my-profile',
            name: 'my-profile',
            component: MyProfile,
          },
          {
            path: '/physical-analysis',
            name: 'physical-analysis',
            component: PhysicalAnalysis 
          },
          {
            path: '/reserves',
            name : 'reserves',
            component: Reserves
          },
          {
            path: '/info-users',
            name: 'info-users',
            component: InfoUsers
          }

          

    ] })


export default router