import { reactive } from "vue";

export const recentPosts = reactive({
    recent: [],
    async PostRecientes(){
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/posts`)
            const all = await res.json()
            this.recent = all
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .slice(0, 5)
        } catch (err) {
            console.error('Error cargando posts recientes:', err)
        }
    }
})