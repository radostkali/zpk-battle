export interface Round {
  id: number;
  number: number;
  theme: string;
  type: string;
  lastDay: string;
  style?: string;
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
