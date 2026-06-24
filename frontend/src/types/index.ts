/** Shared TypeScript types mirroring DRF serializer shapes. */

export interface Genre {
  id: number
  slug: string
  name: string
  movie_count?: number
}

export interface DirectorMinimal {
  id: number
  slug: string
  name: string
  photo_url: string
}

export interface DirectorDetail extends DirectorMinimal {
  bio: string
  birth_date: string | null
  movies: MovieList[]
}

export interface ActorMinimal {
  id: number
  slug: string
  name: string
  photo_url: string
}

export interface ActorDetail extends ActorMinimal {
  bio: string
  birth_date: string | null
  movies: MovieList[]
}

export interface Review {
  id: number
  author_name: string
  rating: number
  comment: string
  created_at: string
}

/** Compact movie shape used in list views. */
export interface MovieList {
  id: number
  slug: string
  title: string
  release_year: number
  poster_url: string
  genres: Genre[]
  director: DirectorMinimal | null
  average_rating: number | null
}

/** Full movie shape used in the detail view. */
export interface MovieDetail extends MovieList {
  synopsis: string
  actors: ActorMinimal[]
  reviews: Review[]
}

/** Paginated response wrapper from DRF PageNumberPagination. */
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/** Query params accepted by the movies endpoint. */
export interface MovieFilters {
  search?: string
  genre_slug?: string
  director_slug?: string
  actor?: number
  release_year?: number
  year_min?: number
  year_max?: number
  ordering?: string
  page?: number
}
