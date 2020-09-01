import Vue from "../../node_modules/vue";
import VueRouter from "../../node_modules/vue-router";
import Main from "../BrandiService/Main/Main.vue";
import Detail from "../BrandiService/Detail/Detail.vue";
import Login from "../BrandiService/Login/Login.vue";
import VueAgile from "vue-agile";
import AdminFrame from "../BrandiAdmin/Components/AdminFrame.vue";
import ProductRegistration from "../BrandiAdmin/ProductRegistration/ProductRegistration.vue";
import Order from "../BrandiService/Order/order.vue";
import Footer from "../BrandiService/Components/Footer.vue";
import ProductManagement from "../BrandiAdmin/ProductRegistration/ProductManagement.vue";
import Mypage from "../BrandiService/Mypage/Mypage.vue";
import OrderList from "../BrandiService/Mypage/OrderList.vue";
import Coupon from "../BrandiService/Mypage/Coupon.vue";
import Point from "../BrandiService/Mypage/Point.vue";
import OrderDetail from "../BrandiService/OrderDetail/OrderDetail.vue";
import UserManagement from "../BrandiAdmin/UserManagement/UserManagement.vue";

Vue.use(VueAgile);
Vue.use(VueRouter);

export const router = new VueRouter({
  mode: "hash",
  routes: [
    {
      path: "/main",
      component: Main,
    },
    {
      path: "/detail",
      component: Detail,
    },
    {
      path: "/login",
      component: Login,
    },
    {
      path: "/order",
      component: Order,
    },
    {
      path: "/mypage",
      redirect: "/mypage/orderList",
      component: Mypage,
      name: Mypage,
      children: [
        {
          path: "",
          redirect: "/mypage/orderList",
          component: OrderList,
          name: "orderList",
        },
        {
          path: "orderList",
          component: OrderList,
          name: "orderList",
        },
        {
          path: "point",
          component: Point,
          name: "point",
        },
        {
          path: "coupon",
          component: Coupon,
          name: "coupon",
        },
        {
          path: "qna",
          component: Mypage,
          name: "qna",
        },
        {
          path: "faq",
          component: Mypage,
          name: "faq",
        },
      ],
    },
    {
      path: "/order/detail",
      component: OrderDetail,
    },
    {
      //초기 url을 main으로 적용
      path: "/",
      redirect: "/main",
    },
    {
      path: "/admin",
      component: AdminFrame,
      name: AdminFrame,
      children: [
        {
          path: "productRegistration",
          component: ProductRegistration,
          name: "productRegistration",
        },
        {
          path: "ProductManagement",
          component: ProductManagement,
          name: "ProductManagement",
        },
        {
          path: "UserManagement",
          component: UserManagement,
          name: "UserManagement",
        },
      ],
    },
    {
      path: "/footer",
      component: Footer,
    },
  ],
});
