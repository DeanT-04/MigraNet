# Configuration Directory

## ⚙️ Description

This directory contains project configuration files and visualization parameter guides.

## 📋 File List

### `gephi_visualization_guide.txt`
**Gephi Visualization Parameter Optimization Guide**

Contains optimized Gephi configuration parameters for the refined network.

## 🎨 Gephi Configuration Details

### Layout Algorithm: ForceAtlas 2

#### Core Parameters:
```
Repulsion Strength: 2000    (2x default, prevents node overlap)
Gravity: 50                  (10x default, keeps network compact)
Prevent Overlap: ✅ Enabled  (mandatory)
Edge Weight Influence: 1.0   (fully considers edge weights)
Runtime: 3-5 minutes         (until network stabilizes)
```

#### Why These Settings?
- **High Repulsion**: 238 nodes need sufficient space
- **High Gravity**: Prevents network from becoming too dispersed
- **Prevent Overlap**: Ensures label readability
- **Edge Weight**: Strongly connected nodes stay closer

---

### Appearance Settings

#### Node Styling
```
Color: By Category field
  - trigger_mechanisms  → Yellow
  - true_comorbidities  → Red
  - social_impact       → Blue
  - interventions       → Green

Size: By Frequency field
  - Min value: 2
  - Max value: 15
  - Algorithm: Linear scaling

Labels: Show only if Frequency > 5
  - Reduces visual clutter
  - Highlights important nodes
```

#### Edge Styling
```
Transparency: 0.3 (30%)
  - Improves readability
  - Reduces overlap obstruction

Thickness: By Weight field
  - Strong associations thicker
  - Weak associations thinner

Color: Gray or inherit source node color
```

---

## 🎯 Usage Steps

### 1. Import Data
```
Gephi → Open → Import node and edge CSV files
```

### 2. Apply Layout
```
Layout panel → Select ForceAtlas 2 → Set parameters → Run
```

### 3. Set Appearance
```
Appearance panel → Nodes → Color → Partition → Category
Appearance panel → Nodes → Size → Ranking → Frequency
```

### 4. Optimize Labels
```
Labels panel → Font size: 12pt
Label Adjust → Prevent overlap
Show labels → High-frequency nodes only
```

### 5. Export Image
```
Preview → Adjust view → Export as PNG/SVG
Recommended size: 4000x3000px (300 DPI)
```

---

## 💡 Advanced Tips

### Community Detection
```
Statistics → Modularity → Run
Appearance → Node color → By Modularity Class
```
**Purpose**: Identify research sub-topic clusters

### Centrality Analysis
```
Statistics → Network Diameter → Run
Statistics → Betweenness Centrality → Run
```
**Purpose**: Find "bridge" concepts

### Filter Application
```
Filters → By Frequency range
Filters → By Category type
```
**Purpose**: Focus on specific sub-networks

---

## 🎨 Color Scheme Suggestions

### Academic Style (Default)
```
Trigger Mechanisms  : #FFC107 (Amber)
True Comorbidities  : #F44336 (Red)
Social Impact       : #2196F3 (Blue)
Interventions       : #4CAF50 (Green)
Background: White
```

### Dark Theme
```
Trigger Mechanisms  : #FFD54F (Light Yellow)
True Comorbidities  : #EF5350 (Light Red)
Social Impact       : #42A5F5 (Light Blue)
Interventions       : #66BB6A (Light Green)
Background: #1E1E1E (Dark Gray)
```

---

## 📊 Expected Visualization Results

### Network Characteristics
- Large central nodes (Quality Life, Treatment Outcome)
- Four colored category clusters
- Clear "star" structures (highly connected nodes)
- Some peripheral small clusters (specific research topics)

### Post-Optimization Benefits
- ✅ No node overlap
- ✅ Clear category boundaries
- ✅ Highlighted core concepts
- ✅ Readable labels

---

## 🔧 Troubleshooting

### Issue: Nodes still overlapping
**Solution**: Increase repulsion strength to 3000-4000

### Issue: Network too dispersed
**Solution**: Increase gravity to 100-150

### Issue: Labels hard to read
**Solution**: 
- Increase font size
- Raise Frequency threshold (show only >10 nodes)

### Issue: Layout runs too slow
**Solution**: 
- Reduce to 3 minutes
- Use simplified layout (YifanHu)

---

## 📖 Reference Resources

- [Gephi Official Documentation](https://gephi.org/users/)
- [ForceAtlas2 Paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679)
- Example images: See `examples/` directory (if available)

---

## ✅ Pre-Visualization Checklist

Before visualization:
- [ ] Data imported correctly
- [ ] Node count = 238
- [ ] Edge count = 863
- [ ] Category field has 4 values
- [ ] Frequency field is numeric
- [ ] Weight field is numeric

---

**Tip**: First-time users should follow parameters exactly. Adjust according to needs after familiarization.
