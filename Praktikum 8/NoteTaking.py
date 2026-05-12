from datetime import datetime
from collections import defaultdict


# ─────────────────────────────────────────────
# 1. NODE: Doubly Linked List untuk Note
# ─────────────────────────────────────────────

class NoteNode:
    """Satu node note dalam doubly linked list."""
    def __init__(self, note_id: str, title: str, content: str):
        self.note_id   = note_id
        self.title     = title
        self.content   = content
        self.tags      = []                        # list of tag strings
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.synced    = False

        # Pointer untuk chronological list
        self.prev_chrono = None
        self.next_chrono = None

        # Pointer untuk alphabetical list
        self.prev_alpha  = None
        self.next_alpha  = None

    def __repr__(self):
        return f"Note(id={self.note_id}, title='{self.title}', tags={self.tags})"


# ─────────────────────────────────────────────
# 2. DOUBLY LINKED LIST (Chronological)
# ─────────────────────────────────────────────

class ChronologicalList:
    """Doubly linked list diurutkan berdasarkan waktu pembuatan (terbaru di depan)."""
    def __init__(self):
        self.head = None  # node terbaru
        self.tail = None  # node terlama

    def insert(self, node: NoteNode):
        """Sisipkan note baru di depan (terbaru)."""
        node.next_chrono = self.head
        node.prev_chrono = None
        if self.head:
            self.head.prev_chrono = node
        self.head = node
        if self.tail is None:
            self.tail = node

    def remove(self, node: NoteNode):
        """Hapus node dari list."""
        if node.prev_chrono:
            node.prev_chrono.next_chrono = node.next_chrono
        else:
            self.head = node.next_chrono

        if node.next_chrono:
            node.next_chrono.prev_chrono = node.prev_chrono
        else:
            self.tail = node.prev_chrono

        node.prev_chrono = node.next_chrono = None

    def traverse(self) -> list:
        """Kembalikan semua note dalam urutan kronologis (terbaru → terlama)."""
        result, cur = [], self.head
        while cur:
            result.append(cur)
            cur = cur.next_chrono
        return result


# ─────────────────────────────────────────────
# 3. DOUBLY LINKED LIST (Alphabetical)
# ─────────────────────────────────────────────

class AlphabeticalList:
    """Doubly linked list diurutkan berdasarkan judul (A → Z)."""
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, node: NoteNode):
        """Sisipkan node pada posisi yang benar secara alfabetis."""
        # Cari posisi yang tepat
        cur = self.head
        while cur and cur.title.lower() <= node.title.lower():
            cur = cur.next_alpha

        if cur is None:
            # Sisipkan di akhir
            node.prev_alpha = self.tail
            node.next_alpha = None
            if self.tail:
                self.tail.next_alpha = node
            self.tail = node
            if self.head is None:
                self.head = node
        elif cur.prev_alpha is None:
            # Sisipkan di awal
            node.prev_alpha = None
            node.next_alpha = self.head
            if self.head:
                self.head.prev_alpha = node
            self.head = node
        else:
            # Sisipkan di tengah
            prev_node = cur.prev_alpha
            node.prev_alpha = prev_node
            node.next_alpha = cur
            prev_node.next_alpha = node
            cur.prev_alpha = node

    def remove(self, node: NoteNode):
        """Hapus node dari list."""
        if node.prev_alpha:
            node.prev_alpha.next_alpha = node.next_alpha
        else:
            self.head = node.next_alpha

        if node.next_alpha:
            node.next_alpha.prev_alpha = node.prev_alpha
        else:
            self.tail = node.prev_alpha

        node.prev_alpha = node.next_alpha = None

    def traverse(self) -> list:
        """Kembalikan semua note dalam urutan alfabetis (A → Z)."""
        result, cur = [], self.head
        while cur:
            result.append(cur)
            cur = cur.next_alpha
        return result


# ─────────────────────────────────────────────
# 4. CIRCULAR BUFFER untuk Sync Tracking
# ─────────────────────────────────────────────

class CircularBuffer:
    """
    Circular buffer berkapasitas tetap untuk melacak perubahan terbaru.
    Setelah penuh, entri paling lama ditimpa.
    """
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.buffer   = [None] * capacity
        self.head     = 0   # indeks tulis berikutnya
        self.size     = 0   # jumlah elemen aktif

    def push(self, event: dict):
        """Tambahkan event perubahan ke buffer."""
        self.buffer[self.head] = event
        self.head = (self.head + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1

    def get_recent(self) -> list:
        """Kembalikan semua event dari yang terbaru ke terlama."""
        result = []
        for i in range(self.size):
            idx = (self.head - 1 - i) % self.capacity
            result.append(self.buffer[idx])
        return result

    def __repr__(self):
        return f"CircularBuffer(capacity={self.capacity}, size={self.size})"


# ─────────────────────────────────────────────
# 5. NOTE MANAGER: Komponen Utama
# ─────────────────────────────────────────────

class NoteManager:
    """
    Mengelola semua note dengan:
    - HashMap untuk akses cepat O(1) by ID
    - HashMap of lists untuk multi-linked by tag
    - Doubly linked list kronologis dan alfabetis
    - Circular buffer untuk sync tracking
    """

    def __init__(self, sync_buffer_size: int = 10):
        # Penyimpanan utama: note_id → NoteNode  (O(1) lookup)
        self.notes: dict[str, NoteNode] = {}

        # Multi-linked by tag: tag → [NoteNode, ...]
        self.tag_index: dict[str, list] = defaultdict(list)

        # Doubly linked lists untuk dua tampilan
        self.chrono_list = ChronologicalList()
        self.alpha_list  = AlphabeticalList()

        # Circular buffer untuk recent changes
        self.sync_buffer = CircularBuffer(sync_buffer_size)

        self._id_counter = 1

    def _generate_id(self) -> str:
        nid = f"note_{self._id_counter:04d}"
        self._id_counter += 1
        return nid

    # ── CREATE ────────────────────────────────
    def add_note(self, title: str, content: str, tags: list[str] = None) -> NoteNode:
        """Buat note baru dan daftarkan ke semua struktur data."""
        note_id = self._generate_id()
        node    = NoteNode(note_id, title, content)

        if tags:
            node.tags = list(set(tags))  # hilangkan duplikat

        # Simpan ke hash map
        self.notes[note_id] = node

        # Daftarkan ke tag index (multi-linked)
        for tag in node.tags:
            self.tag_index[tag].append(node)

        # Masukkan ke kedua linked list
        self.chrono_list.insert(node)
        self.alpha_list.insert(node)

        # Catat event ke sync buffer
        self.sync_buffer.push({
            "event"    : "CREATE",
            "note_id"  : note_id,
            "title"    : title,
            "timestamp": datetime.now().isoformat(),
            "synced"   : False,
        })

        print(f"[+] Note ditambahkan: {node}")
        return node

    # ── READ ──────────────────────────────────
    def get_by_id(self, note_id: str) -> NoteNode | None:
        return self.notes.get(note_id)

    def get_by_tag(self, tag: str) -> list:
        """Kembalikan semua note dengan tag tertentu."""
        return self.tag_index.get(tag, [])

    def view_chronological(self) -> list:
        """Tampilkan semua note (terbaru → terlama)."""
        return self.chrono_list.traverse()

    def view_alphabetical(self) -> list:
        """Tampilkan semua note (A → Z)."""
        return self.alpha_list.traverse()

    # ── UPDATE ────────────────────────────────
    def update_note(self, note_id: str, title: str = None,
                    content: str = None, tags: list[str] = None):
        """Update note; perbarui linked list dan tag index."""
        node = self.notes.get(note_id)
        if not node:
            print(f"[!] Note {note_id} tidak ditemukan.")
            return

        if title and title != node.title:
            # Hapus & masukkan ulang di alpha list (posisi berubah)
            self.alpha_list.remove(node)
            node.title = title
            self.alpha_list.insert(node)

        if content:
            node.content = content

        if tags is not None:
            # Hapus dari tag index lama
            for old_tag in node.tags:
                if node in self.tag_index[old_tag]:
                    self.tag_index[old_tag].remove(node)

            # Daftar tag baru
            node.tags = list(set(tags))
            for new_tag in node.tags:
                self.tag_index[new_tag].append(node)

        node.updated_at = datetime.now()
        node.synced     = False

        # Catat ke sync buffer
        self.sync_buffer.push({
            "event"    : "UPDATE",
            "note_id"  : note_id,
            "timestamp": datetime.now().isoformat(),
            "synced"   : False,
        })
        print(f"[~] Note diperbarui: {node}")

    # ── DELETE ────────────────────────────────
    def delete_note(self, note_id: str):
        """Hapus note dari semua struktur data."""
        node = self.notes.pop(note_id, None)
        if not node:
            print(f"[!] Note {note_id} tidak ditemukan.")
            return

        # Hapus dari tag index
        for tag in node.tags:
            if node in self.tag_index[tag]:
                self.tag_index[tag].remove(node)

        # Hapus dari kedua linked list
        self.chrono_list.remove(node)
        self.alpha_list.remove(node)

        # Catat ke sync buffer
        self.sync_buffer.push({
            "event"    : "DELETE",
            "note_id"  : note_id,
            "timestamp": datetime.now().isoformat(),
            "synced"   : True,   # dianggap langsung sync (sudah tiada)
        })
        print(f"[-] Note dihapus: {note_id}")

    # ── SYNC ──────────────────────────────────
    def mark_synced(self, note_id: str):
        """Tandai note sebagai sudah ter-sync."""
        node = self.notes.get(note_id)
        if node:
            node.synced = True
            print(f"[✓] Note {note_id} ditandai synced.")

    def get_recent_changes(self) -> list:
        """Kembalikan perubahan terbaru dari circular buffer."""
        return self.sync_buffer.get_recent()

    # ── DISPLAY ───────────────────────────────
    def display_all(self):
        print("\n" + "=" * 55)
        print("  TAMPILAN KRONOLOGIS (Terbaru → Terlama)")
        print("=" * 55)
        for i, n in enumerate(self.view_chronological(), 1):
            synced = "✓" if n.synced else "✗"
            print(f"  {i}. [{synced}] {n.title!r:25s} tags={n.tags}")

        print("\n" + "=" * 55)
        print("  TAMPILAN ALFABETIS (A → Z)")
        print("=" * 55)
        for i, n in enumerate(self.view_alphabetical(), 1):
            print(f"  {i}. {n.title!r:25s} id={n.note_id}")

        print("\n" + "=" * 55)
        print("  RECENT CHANGES (Circular Buffer)")
        print("=" * 55)
        for ev in self.get_recent_changes():
            print(f"  [{ev['event']:6s}] {ev['note_id']} @ {ev['timestamp'][:19]}")
        print()


# ─────────────────────────────────────────────
# 6. DEMO / DRIVER CODE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════╗")
    print("║   Note-Taking App — Demo Struktur Data           ║")
    print("╚══════════════════════════════════════════════════╝\n")

    mgr = NoteManager(sync_buffer_size=8)

    # Tambah beberapa note
    n1 = mgr.add_note("Belajar Python",    "Dasar-dasar Python",        tags=["python", "belajar"])
    n2 = mgr.add_note("Algoritma Sorting", "Bubble, Merge, Quick Sort", tags=["algoritma", "belajar"])
    n3 = mgr.add_note("Catatan Rapat",     "Agenda minggu ini",         tags=["kerja"])
    n4 = mgr.add_note("Resep Nasi Goreng", "Bahan dan cara masak",      tags=["masak", "resep"])
    n5 = mgr.add_note("Agenda Liburan",    "Rencana ke Bali",           tags=["liburan", "rencana"])

    # Cari note berdasarkan tag
    print("\n── Notes dengan tag 'belajar' ──")
    for n in mgr.get_by_tag("belajar"):
        print(f"   → {n}")

    # Update note
    mgr.update_note(n1.note_id, title="Belajar Python & OOP", tags=["python", "belajar", "oop"])

    # Tandai sebagai synced
    mgr.mark_synced(n2.note_id)
    mgr.mark_synced(n3.note_id)

    # Hapus satu note
    mgr.delete_note(n4.note_id)

    # Tampilkan semua view
    mgr.display_all()

    # Cek tag index setelah update
    print("── Notes dengan tag 'oop' (setelah update) ──")
    for n in mgr.get_by_tag("oop"):
        print(f"   → {n}")