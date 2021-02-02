export interface Round {
  id: number;
  number: number;
  theme: string;
  type: string;
  lastDay: number;
  style?: string;
  tracks: Track[];
}

export interface Track {
  id: number;
  name: string;
  userId: number;
  userUsername: string;
  rates: Rate[];
}

export interface Rate {
  categoryId: number;
  userId: number;
  userUsername: string;
}

export interface Category {
  id: number;
  name: string;
}
