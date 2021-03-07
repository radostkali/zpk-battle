export interface Round {
  id: number;
  number: number;
  theme: string;
  type: 'one_vs_one' | 'all_vs_all';
  lastDay: string;
  style?: string;
  isExpired: boolean;
  tracks: Track[];
  pairs: Pair[];
}

export interface Pair {
  tracks: Track[];
}

export interface Track {
  id: number;
  name: string;
  userId: number;
  userUsername: string;
  userColor: string;
  rates: Rate[];
}

export interface Rate {
  categoryId: number;
  userId: number;
  userUsername: string;
  userColor: string;
}

export interface Category {
  id: number;
  name: string;
}
