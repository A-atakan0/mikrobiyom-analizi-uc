import pandas as pd
import numpy as np
import glob
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

# --- Her ornegin rel-abundance dosyasini oku ve birlestir ---
files = sorted(glob.glob("results/emu/*/*_rel-abundance.tsv"))
# Esik degerli dosyalari (threshold) disla, sadece ana dosyayi al
files = [f for f in files if "threshold" not in f]

abundance_dict = {}
for f in files:
    sample = os.path.basename(f).replace("_rel-abundance.tsv", "")
    df = pd.read_csv(f, sep="\t")
    df = df.dropna(subset=["species"])
    series = df.groupby("species")["abundance"].sum()
    abundance_dict[sample] = series

combined = pd.DataFrame(abundance_dict).fillna(0)
combined.to_csv("results/combined_species_abundance.csv")
print("Birlesmis tablo boyutu:", combined.shape)
print("Ornekler:", list(combined.columns))

# --- Grup etiketleri ---
mes0_samples = [os.path.basename(f).split('.')[0] for f in os.listdir("data/filtered/MES_0")]
mes3_samples = [os.path.basename(f).split('.')[0] for f in os.listdir("data/filtered/MES_3")]
groups = {s: ("MES_0" if s in mes0_samples else "MES_3") for s in combined.columns}
print("\nGrup atamasi:")
for s, g in groups.items():
    print(f"  {s}: {g}")

# --- Shannon cesitlilik indeksi (manuel hesaplama) ---
def shannon_index(counts):
    p = counts[counts > 0]
    p = p / p.sum()
    return -np.sum(p * np.log(p))

shannon_scores = {s: shannon_index(combined[s].values) for s in combined.columns}
shannon_df = pd.DataFrame.from_dict(shannon_scores, orient='index', columns=['shannon'])
shannon_df['group'] = [groups[s] for s in shannon_df.index]
print("\nShannon cesitlilik indeksi:")
print(shannon_df.sort_values('group'))

mes0_vals = shannon_df[shannon_df['group']=='MES_0']['shannon']
mes3_vals = shannon_df[shannon_df['group']=='MES_3']['shannon']
stat, pval = mannwhitneyu(mes0_vals, mes3_vals)
print(f"\nMann-Whitney U testi (MES_0 vs MES_3 Shannon cesitliligi): p={pval:.4f}")

# --- Gorsellestirme 1: Shannon cesitlilik kutu grafik ---
plt.figure(figsize=(6,5))
sns.boxplot(data=shannon_df, x='group', y='shannon', hue='group',
            palette={'MES_0':'#3498db','MES_3':'#e74c3c'}, legend=False)
sns.stripplot(data=shannon_df, x='group', y='shannon', color='black', alpha=0.7, size=8)
plt.title(f"Shannon Cesitlilik Indeksi\n(Mann-Whitney p={pval:.4f})")
plt.ylabel("Shannon Indeksi")
plt.tight_layout()
plt.savefig("figures/shannon_diversity.png", dpi=300)
plt.close()

# --- Gorsellestirme 2: En bol 15 turun bar plot'u ---
top15 = combined.sum(axis=1).sort_values(ascending=False).head(15).index
plot_data = combined.loc[top15].T
plot_data['group'] = [groups[s] for s in plot_data.index]
plot_data = plot_data.sort_values('group')

fig, ax = plt.subplots(figsize=(13,7))
plot_data.drop('group', axis=1).plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
ax.set_ylabel("Goreceli Bolluk")
ax.set_xlabel("Ornek")
ax.set_title("En Bol 15 Turun Ornek Bazinda Dagilimi (MES_0 vs MES_3)")
plt.legend(bbox_to_anchor=(1.02,1), loc='upper left', fontsize=7)
plt.tight_layout()
plt.savefig("figures/taxa_barplot.png", dpi=300)
plt.close()

print("\nGorseller kaydedildi: figures/shannon_diversity.png, figures/taxa_barplot.png")
