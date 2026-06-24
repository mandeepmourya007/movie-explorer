import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'movies',
      component: () => import('@/views/MoviesView.vue'),
    },
    {
      path: '/movies/:slug',
      name: 'movie-detail',
      component: () => import('@/views/MovieDetailView.vue'),
    },
    {
      path: '/actors/:slug',
      name: 'actor-detail',
      component: () => import('@/views/ActorDetailView.vue'),
    },
    {
      path: '/directors/:slug',
      name: 'director-detail',
      component: () => import('@/views/DirectorDetailView.vue'),
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('@/views/FavoritesView.vue'),
    },
  ],
  scrollBehavior(_to, _from, savedPosition) {
    return savedPosition ?? { top: 0 }
  },
})

export default router
