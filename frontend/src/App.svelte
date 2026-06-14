<script lang='ts'>
import { onMount } from 'svelte';

const BASE_URL = '/api';

let models: string[] = [];
let selectedModelPath = '';
let modelType = 'stablediffusion';

let modelId = '';
let pipelineId = '';
let prompt = '';
let generatedImageUrl = '';

let statusMessage = '';
let isLoading = false;

onMount(async () => {
  try {
    statusMessage = 'Fetching model list...';
    const res = await fetch(`${BASE_URL}/list_models/stablediffusion`);
    if (!res.ok) throw new Error('Failed to get model list');
    models = await res.json();
    if (models.length > 0) selectedModelPath = models[0];
    statusMessage = '';
  } catch (err: any) {
    statusMessage = `Error: ${err.message}`;
  }
});

async function setupPipeline() {
  if (!selectedModelPath) return;
  isLoading = true;
  statusMessage = 'Loading model...';

  try {
    const loadRes = await fetch(`${BASE_URL}/load`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: modelType, path: selectedModelPath })
    });
    if (!loadRes.ok) throw new Error('Failed to load model');
    const loadData = await loadRes.json();
    modelId = loadData.model_id;

    statusMessage = 'Creating pipeline...';
    const pipeRes = await fetch(`${BASE_URL}/create_pipeline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_id: modelId, type: modelType })
    });
    if (!pipeRes.ok) throw new Error('Failed to create pipeline');
    const pipeData = await pipeRes.json();
    pipelineId = pipeData.pipeline_id;

    statusMessage = 'Ready.';
  } catch (err: any) {
    statusMessage = `Error: ${err.message}`;
  } finally {
    isLoading = false;
  }
}

async function generateImage() {
  if (!pipelineId || !prompt) return;
  isLoading = true;
  statusMessage = 'Generating...';
  if (generatedImageUrl) {
    URL.revokeObjectURL(generatedImageUrl);
    generatedImageUrl = '';
  }

  try {
    const res = await fetch(`${BASE_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pipeline_id: pipelineId, prompt: prompt })
    });

    if (!res.ok) throw new Error('Failed to generate image');

    const blob = await res.blob();
    generatedImageUrl = URL.createObjectURL(blob);
    statusMessage = 'Generation done.';
  } catch (err: any) {
    statusMessage = `Error: ${err.message}`;
  } finally {
    isLoading = false;
  }
}
</script>

<main class="container">
  <h1>tinypalette</h1>

  {#if statusMessage}
    <div class="status-box">{statusMessage}</div>
  {/if}

  <section class="card">
    <h2>1. Model setup</h2>
    <div class="form-group">
      <label for="model-select">Select model:</label>
      <select id="model-select" bind:value={selectedModelPath} disabled={isLoading || !!pipelineId}>
        {#each models as model}
          <option value={model}>{model.split('/').pop() || model}</option>
        {/each}
      </select>
    </div>

    <button on:click={setupPipeline} disabled={isLoading || !selectedModelPath || !!pipelineId}>
      {pipelineId ? 'setup done' : 'load a model'}
    </button>

    {#if pipelineId}
      <p class="success-text">Pipeline ID: <code>{pipelineId}</code></p>
    {/if}
  </section>

  <section class="card" class:disabled={!pipelineId}>
    <h2>2. Generation</h2>
    <div class="form-group">
      <label for="prompt-input">Prompt:</label>
      <textarea
        id="prompt-input"
        bind:value={prompt}
        placeholder="a fantasy landscape, highly detailed..."
        disabled={!pipelineId || isLoading}
      ></textarea>
    </div>

    <button on:click={generateImage} disabled={!pipelineId || !prompt || isLoading}>
      {isLoading ? 'Generating...' : 'Generate'}
    </button>
  </section>

  <section class="result-container">
    {#if generatedImageUrl}
      <div class="image-wrapper">
        <img src={generatedImageUrl} alt="Generated" />
      </div>
    {:else if isLoading && pipelineId}
      <div class="spinner-placeholder">Generating an image...</div>
    {/if}
  </section>
</main>

<style>
:global(body) {
  font-family: sans-serif;
  background-color: #f5f7fa;
  color: #333;
  margin: 0;
  padding: 20px;
}
.container {
  max-width: 800px;
  margin: 0 auto;
}
.card {
  background: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
textarea {
  height: 100px;
  resize: vertical;
}
button {
  background-color: #0070f3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.status-box {
  background-color: #e1f5fe;
  border-left: 4px solid #0288d1;
  padding: 12px;
  margin-bottom: 20px;
  border-radius: 4px;
}
.success-text {
  color: #2e7d32;
  font-size: 14px;
}
.result-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
.image-wrapper img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
.spinner-placeholder {
  padding: 40px;
  background: #eaeaea;
  border-radius: 8px;
  width: 100%;
  text-align: center;
}
</style>
