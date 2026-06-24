import type {
  ActorDetail,
  ActorMinimal,
  DirectorDetail,
  DirectorMinimal,
  Genre,
  MovieDetail,
  MovieFilters,
  MovieList,
  PaginatedResponse,
} from '@/types'
import client from './client'

// ---------------------------------------------------------------------------
// Movies
// ---------------------------------------------------------------------------

export const fetchMovies = (params: MovieFilters = {}): Promise<PaginatedResponse<MovieList>> =>
  client.get<PaginatedResponse<MovieList>>('/movies/', { params }).then((r) => r.data)

export const fetchMovie = (slug: string): Promise<MovieDetail> =>
  client.get<MovieDetail>(`/movies/${slug}/`).then((r) => r.data)

/** Fetch multiple movies by slug (used by FavoritesView). */
export const fetchMoviesBySlugs = async (slugs: string[]): Promise<MovieList[]> => {
  if (!slugs.length) return []
  const results = await Promise.all(slugs.map((slug) => fetchMovie(slug)))
  return results
}

// ---------------------------------------------------------------------------
// Actors
// ---------------------------------------------------------------------------

export const fetchActors = (params: Record<string, unknown> = {}): Promise<PaginatedResponse<ActorMinimal>> =>
  client.get<PaginatedResponse<ActorMinimal>>('/actors/', { params }).then((r) => r.data)

export const fetchActor = (slug: string): Promise<ActorDetail> =>
  client.get<ActorDetail>(`/actors/${slug}/`).then((r) => r.data)

// ---------------------------------------------------------------------------
// Directors
// ---------------------------------------------------------------------------

export const fetchDirectors = (
  params: Record<string, unknown> = {}
): Promise<PaginatedResponse<DirectorMinimal>> =>
  client.get<PaginatedResponse<DirectorMinimal>>('/directors/', { params }).then((r) => r.data)

export const fetchDirector = (slug: string): Promise<DirectorDetail> =>
  client.get<DirectorDetail>(`/directors/${slug}/`).then((r) => r.data)

// ---------------------------------------------------------------------------
// Genres
// ---------------------------------------------------------------------------

export const fetchGenres = (): Promise<PaginatedResponse<Genre>> =>
  client.get<PaginatedResponse<Genre>>('/genres/', { params: { page_size: 100 } }).then((r) => r.data)
