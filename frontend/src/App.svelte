<script lang='ts'>
import { onMount } from 'svelte';
import ToastContainer from './lib/ToastContainer.svelte';
import { addToast } from './lib/toastStore';

const BASE_URL = '/api';

let models: string[] = [];
let selectedModelPath = '';
let modelType = 'stablediffusion';

let modelId = '';
let pipelineId = '';
let prompt = '';
let negative_prompt = '';
let generatedImageUrl = '';

let generatedImages: string[] = [];

let isLoading = false;

const fetchGeneratedImages = async () => {
  try {
    addToast({ type: 'info', message: 'Fetching generated images...' });
    const res = await fetch(`${BASE_URL}/list_outputs/images`);
    if (!res.ok) throw new Error('Failed to get generated images');
    generatedImages = await res.json();
  } catch (err: any) {
    addToast({ type: 'error', message: `Error: ${err.message}` });
  }
};

onMount(async () => {
  try {
    addToast({ type: 'info', message: 'Fetching model list...' });
    const res = await fetch(`${BASE_URL}/list_models/stablediffusion`);
    if (!res.ok) throw new Error('Failed to get model list');
    models = await res.json();
    if (models.length > 0) selectedModelPath = models[0];
  } catch (err: any) {
    addToast({ type: 'error', message: `Error: ${err.message}` });
  }
  await fetchGeneratedImages();
});

async function setupPipeline() {
  if (!selectedModelPath) return;
  isLoading = true;
  addToast({ type: 'info', message: 'Loading model...' });

  try {
    const loadRes = await fetch(`${BASE_URL}/load`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: modelType, path: selectedModelPath })
    });
    if (!loadRes.ok) throw new Error('Failed to load model');
    const loadData = await loadRes.json();
    modelId = loadData.model_id;

    addToast({ type: 'info', message: 'Creating pipeline...' });
    const pipeRes = await fetch(`${BASE_URL}/create_pipeline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_id: modelId, type: modelType })
    });
    if (!pipeRes.ok) throw new Error('Failed to create pipeline');
    const pipeData = await pipeRes.json();
    pipelineId = pipeData.pipeline_id;

    addToast({ type: 'info', message: 'Ready.' });
  } catch (err: any) {
    addToast({ type: 'error', message: `Error: ${err.message}` });
  } finally {
    isLoading = false;
  }
}

async function generateImage() {
  if (!pipelineId || !prompt) return;
  isLoading = true;
  addToast({ type: 'info', message: 'Generating...' });
  if (generatedImageUrl) {
    URL.revokeObjectURL(generatedImageUrl);
    generatedImageUrl = '';
  }

  try {
    const res = await fetch(`${BASE_URL}/generate/text2image`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pipeline_id: pipelineId, prompt, negative_prompt })
    });

    if (!res.ok) throw new Error('Failed to generate image');

    const blob = await res.blob();
    generatedImageUrl = URL.createObjectURL(blob);
    addToast({ type: 'info', message: 'Generation done.' });
  } catch (err: any) {
    addToast({ type: 'error', message: `Error: ${err.message}` });
  } finally {
    isLoading = false;
    await fetchGeneratedImages();
  }
}
</script>

<main class="container">
  <div class='left'>
    <section class="card">
      <div class="form-group">
        <label for="model-select">Select model:</label>
        <select id="model-select" bind:value={selectedModelPath} disabled={isLoading || !!pipelineId}>
          {#each models as model}
            <option value={model}>{model.split('/').pop() || model}</option>
          {/each}
        </select>
      </div>

      <button onclick={setupPipeline} disabled={isLoading || !selectedModelPath || !!pipelineId}>
        {pipelineId ? 'setup done' : 'load a model'}
      </button>
    </section>

    <section class="card" class:disabled={!pipelineId}>
      <div class="form-group">
        <label for="prompt-input">Prompt:</label>
        <textarea
          id="prompt-input"
          bind:value={prompt}
          placeholder="a fantasy landscape, highly detailed..."
          disabled={!pipelineId || isLoading}
        ></textarea>
        <label for="negativeprompt-input">Negative Prompt:</label>
        <textarea
          id="negativeprompt-input"
          bind:value={negative_prompt}
          placeholder="bad fingers..."
          disabled={!pipelineId || isLoading}
        ></textarea>
      </div>

      <button onclick={generateImage} disabled={!pipelineId || !prompt || isLoading}>
        {isLoading ? 'Generating...' : 'Generate'}
      </button>
    </section>
  </div>
  <div class='center'>
    <input type='radio' name="tab-group" id='tab-generation' checked />
    <input type='radio' name="tab-group" id='tab-gallery' />
    <div class='tabbar'>
      <label for='tab-generation'>Generation</label>
      <label for='tab-gallery'>Gallery</label>
    </div>
    <div class='tab-contents'>
      <div class='tab-content' id='tab-generation-content'>
        <section class='result-container'>
          {#if generatedImageUrl}
            <div class="image-wrapper">
              <img src={generatedImageUrl} alt="Generated" />
            </div>
          {:else if isLoading && pipelineId}
            <div class="spinner-placeholder">Generating an image...</div>
          {/if}
        </section>
      </div>
      <div class='tab-content' id='tab-gallery-content'>
        <button onclick={fetchGeneratedImages}>⟳ reload</button>
        <div class='generated-images'>
          {#each generatedImages as i}
            <div class='generated-image'><img src='/data/outputs/images/{i}' loading='lazy' height="150px" width="150px" /></div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</main>

<ToastContainer />

<style>
:root {
  --color-main: #1e1e1e;
  --color-sub: #333;
  --color-extra: #181818;
  --color-text: #ccc;
  --color-accent: #007acc;
  --color-white: #eaeaea;

  --padding-basic: 8px 17px;
}

:global(body) {
  font-family: sans-serif;
  background-color: var(--color-main);
  color: var(--color-text);
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  box-sizing: border-box;
  /*overflow: hidden;*/
}

.container {
  display: grid;
  grid-template-areas: "left center";
  grid-template-columns: minmax(0, 500px) 1fr;
  min-width: 100%;
  height: 100vh;
  margin: 0 auto;
}

.left {
  grid-area: left;
  max-width: 500px;
  background-color: var(--color-extra);
  height: 100%;
  min-height: 0;
  overflow-y: auto;
}

.tabbar {
  user-select: none;
  display: flex;
  border-bottom: 1px solid var(--color-sub);
  padding-left: 4px;
  position: sticky;
  flex-shrink: 0;
}

.tabbar > label {
  padding: var(--padding-basic);
  cursor: pointer;
  background: var(--color-extra);
  border: 1px solid var(--color-sub);
  border-bottom: none;
  margin-right: 5px;
  border-radius: 4px 4px 0 0;
}

input[name='tab-group'] {
  display: none;
}

.tab-contents {
  flex-grow: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding-left: 20px;
}

.tab-content {
  display: none;
  overflow-y: auto;
  /*flex-grow: 1;*/
  height: 100%;
  box-sizing: border-box;
}

#tab-generation:checked ~ .tabbar > label[for="tab-generation"],
#tab-gallery:checked ~ .tabbar > label[for="tab-gallery"] {
  background-color: var(--color-main);
  border-bottom: 1px solid var(--color-sub);
  margin-bottom: -1px;
  font-weight: bold;
}

#tab-generation:checked ~ div.tab-contents > #tab-generation-content,
#tab-gallery:checked ~ div.tab-contents > #tab-gallery-content {
  display: flex;
  flex-direction: column;
}

.center {
  grid-area: center;
  width: 100%;
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.generated-images {
  display: flex;
  flex-wrap: wrap;
}

.generated-image {
  height: 150px;
  width: 150px;
}

.generated-image > img {
  object-fit: cover;
}

.card {
  background: var(--color-extra);
  padding: 20px;
  margin-bottom: 20px;
}
.card.disabled {
  opacity: 0.5;
  pointer-events: none;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--color-sub);
  border-radius: 4px;
  box-sizing: border-box;
  color: inherit;
  background-color: var(--color-main);
}
textarea {
  height: 100px;
  resize: vertical;
}
button {
  background-color: var(--color-accent);
  color: var(--color-sub);
  border: none;
  padding: var(--padding-basic);
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
button:disabled {
  background-color: var(--color-text);
  cursor: not-allowed;
}
.result-container {
  margin: auto;
  display: flex;
  justify-content: center;
  height: 100%;
}
.image-wrapper img {
  max-width: 100%;
  height: auto;
}
.spinner-placeholder {
  padding: 40px;
  background: var(--color-white);
  border-radius: 8px;
  width: 100%;
  text-align: center;
}
</style>
