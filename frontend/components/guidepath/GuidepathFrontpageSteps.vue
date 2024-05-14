<template>
  <div>
    <div v-if="!authStore.loggedIn" class="lg:border-b lg:border-t lg:border-gray-200">
      <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label="Progress">
        <ol role="list" class="overflow-hidden rounded-md lg:flex lg:rounded-none lg:border-l lg:border-r lg:border-gray-200">
          <li v-for="(step, stepIdx) in steps" :key="step.id" class="relative overflow-hidden lg:flex-1">
            <button @click.prevent="submit(step.request)"
              :class="[stepIdx === 0 ? 'rounded-t-md border-b-0' : '', stepIdx === steps.length - 1 ? 'rounded-b-md border-t-0' : '', 'overflow-hidden border border-gray-200 lg:border-0']"
              :disabled="step.disabled">
              <span class="group">
                <span class="absolute left-0 top-0 h-full w-1 bg-transparent group-hover:bg-gray-200 lg:bottom-0 lg:top-auto lg:h-1 lg:w-full" aria-hidden="true" />
                <span class="flex justify-center py-2 text-sm font-medium">
                    <span :class="[
                      step.disabled 
                      ? 'text-kashmir-500 border-kashmir-300' 
                      : 'bg-spring-500 border-spring-500 text-white', 
                      'flex h-8 w-8 items-center justify-center rounded-full border-2'
                      ]">
                        <span>{{ step.id }}</span>
                    </span>
                </span>
                <span class="mx-3 mb-1 flex min-w-0 flex-col">
                    <span class="text-sm text-gray-500">{{ step.description }}</span>
                </span>
              </span>
              <template v-if="stepIdx !== 0">
                <!-- Separator -->
                <div class="absolute inset-0 left-0 top-0 hidden w-3 lg:block" aria-hidden="true">
                    <svg class="h-full w-full text-gray-300" viewBox="0 0 12 82" fill="none" preserveAspectRatio="none">
                    <path d="M0.5 0V31L10.5 41L0.5 51V82" stroke="currentcolor" vector-effect="non-scaling-stroke" />
                    </svg>
                </div>
              </template>
            </button>
          </li>
        </ol>
      </nav>
    </div>
    <div class="mt-4">
      <GuidepathStartPersonalJourney v-if="authStore.loggedIn && !authStore.completedPathway" />
      <GuidepathStartStudyJourney v-if="authStore.loggedIn && authStore.completedPathway" />
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { IKeyable } from "@/interfaces"
import { useAuthStore, usePathwayStore } from "@/stores"

const { t } = useI18n()
const localePath = useLocalePath()
const authStore = useAuthStore()
const pathwayStore = usePathwayStore()
const steps: IKeyable[] = [
      { 
        id: "01", 
        description: t("frontpage.steps.one"), 
        request: "login", disabled: authStore.loggedIn},
      // { 
      //   id: "02", 
      //   description: t("frontpage.steps.two"), 
      //   request: "personal", disabled: !authStore.loggedIn || (authStore.loggedIn && authStore.completedPathway)},
      { 
        id: "02", 
        description: t("frontpage.steps.three"), 
        request: "study", disabled: !authStore.loggedIn || (authStore.loggedIn && !authStore.completedPathway)},
  ]

// WATCHERS
async function submit(request: string) {
    switch (request) {
        case "login":
          return await navigateTo(localePath(`/login`))
        case "personal":
          await pathwayStore.getPersonalTerm()
          if (pathwayStore.termPersonal)
            return await navigateTo(localePath(`/journey/${pathwayStore.termPersonal}`))
          else return await navigateTo(localePath(`/journey/${authStore.profile.id}`))
        case "study":
          await pathwayStore.getFeaturedTerm()
          if (pathwayStore.termStudy)
            return await navigateTo(localePath(`/pathway/${pathwayStore.termStudy}`))
          break
    }
}
</script>