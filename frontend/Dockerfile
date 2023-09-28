FROM node:18.17 AS build
ENV NODE_ENV=development APP_ENV=development NITRO_HOST=${NUXT_HOST:-0.0.0.0} NITRO_PORT=${NUXT_PORT:-3000} NUXT_TELEMETRY_DISABLED=1
# ENV PATH /frontend/node_modules/.bin:$PATH
COPY . /frontend
WORKDIR /frontend
RUN yarn install --frozen-lockfile --network-timeout 100000 --non-interactive
RUN yarn build --standalone
EXPOSE ${NUXT_PORT}

FROM build AS run-dev
# ENTRYPOINT ["yarn"]
CMD ["yarn", "dev"]

FROM build AS run-start
ENV NODE_ENV=production APP_ENV=production
ENTRYPOINT ["yarn"]
CMD ["start"]

FROM node:18.17-alpine AS run-minimal
ARG NUXT_VERSION=^3.5.0
ARG ASPECT_RATIO_VERSION=^0.4.2
ARG AUTOPREFIXER_VERSION=^10.4.13
ARG BROWSER_FS_ACCESS_VERSION=^0.35.0
ARG DAYJS_VERSION=^1.11.9
ARG FORMS_VERSION=^0.5.3
ARG HEADLESSUI_VERSION=^1.7.3
ARG I18N_ISO_COUNTRIES=^7.7.0
ARG I18N_VERSION=^8.0.0-beta.13
ARG NUXT_CONTENT_VERSION=^2.4.3
ARG NUXT_ROBOTS_VERSION=^3.0.0
ARG PHOSPHORICONS_VERSION=^2.1.6
ARG PINI_NUXT_VERSION=^0.4.11
ARG PINIA_PERSISTED_VERSION=^1.0.0
ARG PINIA_VERSION=^2.1.4
ARG POSTCSS_VERSION=^8.4.18
ARG QR_CODE_VERSION=^3.3.3
ARG TAILWINDCSS_VERSION=^3.2.1
ARG TYPOGRAPHY_VERSION=^0.5.7
ARG VEE_I18N_VERSION=^4.7.3
ARG VEE_RULES_VERSION=^4.7.3
ARG VEE_VERSION=^4.7.3
ARG VITE_PWA_NUXT_VERSION=^0.1.0
ARG VUE_TAILWIND_PICKER_VERSION=^1.4.6
ENV NODE_ENV=production APP_ENV=production NITRO_HOST=${NUXT_HOST:-0.0.0.0} NITRO_PORT=${NUXT_PORT:-3000} NUXT_TELEMETRY_DISABLED=1
WORKDIR /frontend
RUN yarn add nuxt@${NUXT_VERSION} @nuxt/content@${NUXT_CONTENT_VERSION} tailwindcss@${TAILWINDCSS_VERSION} autoprefixer@${AUTOPREFIXER_VERSION} postcss@${POSTCSS_VERSION} @tailwindcss/aspect-ratio@${ASPECT_RATIO_VERSION} @tailwindcss/forms@${FORMS_VERSION} @tailwindcss/typography@${TYPOGRAPHY_VERSION} @headlessui/vue@${HEADLESSUI_VERSION} @phosphor-icons/vue@${PHOSPHORICONS_VERSION} pinia@${PINIA_VERSION} @pinia/nuxt@${PINI_NUXT_VERSION} @pinia-plugin-persistedstate/nuxt@${PINIA_PERSISTED_VERSION} vee-validate@${VEE_VERSION} @vee-validate/i18n@${VEE_I18N_VERSION} @vee-validate/rules@${VEE_RULES_VERSION} qrcode.vue@${QR_CODE_VERSION} @nuxtjs/i18n@${I18N_VERSION} @nuxtjs/robots@${NUXT_ROBOTS_VERSION} @vite-pwa/nuxt@${VITE_PWA_NUXT_VERSION} browser-fs-access@${BROWSER_FS_ACCESS_VERSION} dayjs@${DAYJS_VERSION} i18n-iso-countries@${I18N_ISO_COUNTRIES} @nuxtjs/robots@${NUXT_ROBOTS_VERSION} vue-tailwind-datepicker@${VUE_TAILWIND_PICKER_VERSION}
COPY --from=build /app/.nuxt ./.nuxt
COPY --from=build /app/.output/ ./.output
COPY --from=build /app/api ./api
COPY --from=build /app/assets ./assets
COPY --from=build /app/components ./components
COPY --from=build /app/config ./config
COPY --from=build /app/content ./content
COPY --from=build /app/interfaces ./interfaces
COPY --from=build /app/layouts ./layouts
COPY --from=build /app/locales ./locales
COPY --from=build /app/middleware ./middleware
COPY --from=build /app/pages ./pages
COPY --from=build /app/plugins ./plugins
COPY --from=build /app/public ./public
COPY --from=build /app/stores ./stores
COPY --from=build /app/utilities ./utilities
COPY --from=build /app/.env ./
COPY --from=build /app/app.vue ./
COPY --from=build /app/nuxt.config* ./
COPY --from=build /app/tailwind.config* ./
COPY --from=build /app/tsconfig.json* ./
ENTRYPOINT [ "yarn" ]
CMD [ "start" ]
