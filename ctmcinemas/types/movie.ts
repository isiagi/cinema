export interface MovieShowtime {
  time: string
  type: string
  price: string
}

export interface MovieDay {
  date: string
  displayDate: string
  showtimes: MovieShowtime[]
}

export interface MovieDetails {
  id: string
  title: string
  duration: string
  language: string
  rating: string
  description: string
  longDescription: string
  bannerImage: string
  trailerUrl: string
  director: string
  cast: string[]
  genre: string[]
  days: MovieDay[]
  actor: string[]
  image: string
  highlight: string[]
  releaseDate: string
}

