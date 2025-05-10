import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { importProvidersFrom } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

bootstrapApplication(AppComponent, {
  providers: [
    // Ensure HttpClientModule is imported and HttpClient is available for use in the app
    importProvidersFrom(HttpClientModule),
    provideHttpClient()
  ]
}).catch(err => console.error(err));
