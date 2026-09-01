export interface CurrentUser {
  id: string;
  email: string;
}

export interface BuildLogEntry {
  id: string;
  timestamp: string;
  step: string;
  title: string;
  description: string;
}
