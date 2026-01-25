// config.example.js (SECURITY-CLEAN)

class AppConfig {
  constructor() {
    this.environment = this.detectEnvironment();
    this.settings = this.loadSettings();
  }

  detectEnvironment() {
    const hostname = window.location.hostname;

    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "development";
    }

    return "production";
  }

  loadSettings() {
    return {
      development: {
        API_BASE_URL: "",
        DEBUG: true
      },
      production: {
        API_BASE_URL: "/api",
        DEBUG: false
      }
    }[this.environment];
  }

  get(key) {
    return this.settings[key];
  }

  api(endpoint) {
    return `${this.settings.API_BASE_URL}${endpoint}`;
  }
}

window.AppConfig = new AppConfig();
window.API_BASE_URL = window.AppConfig.get("API_BASE_URL");
