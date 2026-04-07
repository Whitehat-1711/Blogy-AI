import { useEffect, useState } from "react";
import BlogGenPage from "./BlogGenPage";
import HumanizePage from "./HumanizePage";
import JournalPage from "./JournalPage";
import LandingPage from "./Landing";
import LoginPage from "./Login";
import SEOAuditPage from "./SEOAuditPage";
import SerpPage from "./SerpPage";
import { WorkflowProvider } from "./context/WorkflowContext";

const pageRegistry = {
  landing: LandingPage,
  login: LoginPage,
  journal: JournalPage,
  "blog-gen": BlogGenPage,
  "strategic-map": SerpPage,
  humanizer: HumanizePage,
  "seo-audit": SEOAuditPage,
};

function RouterShell() {
  const [currentPage, setCurrentPage] = useState("landing");
  const [authUser, setAuthUser] = useState(null);

  // 🔥 GLOBAL STATE
  const [keyword, setKeyword] = useState("");
  const [blogData, setBlogData] = useState(null);
  const [serpData, setSerpData] = useState(null);
  const [loading, setLoading] = useState(false);

  const ActivePage = pageRegistry[currentPage] || LandingPage;
  const protectedPages = new Set(["journal", "blog-gen", "strategic-map", "humanizer", "seo-audit"]);

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem("blogy:user");
      if (raw) {
        setAuthUser(JSON.parse(raw));
      }
    } catch {
      setAuthUser(null);
    }
  }, []);

  const handleNavigate = (page) => {
    let effectiveUser = authUser;
    if (!effectiveUser) {
      try {
        const raw = window.localStorage.getItem("blogy:user");
        if (raw) {
          effectiveUser = JSON.parse(raw);
          setAuthUser(effectiveUser);
        }
      } catch {
        effectiveUser = null;
      }
    }
    if (page === "login" || page === "landing") {
      setCurrentPage(page);
      return;
    }
    if (protectedPages.has(page) && !effectiveUser) {
      setCurrentPage("login");
      return;
    }
    setCurrentPage(page);
  };

  const handleLogout = () => {
    try {
      window.localStorage.removeItem("blogy:user");
    } catch {
      // no-op
    }
    setAuthUser(null);
    setCurrentPage("landing");
  };

  // 🔥 BLOG GENERATION (supports SERP injection)
  const generateBlog = async (overrideData = {}) => {
    try {
      const finalKeyword = overrideData.keyword || keyword;

      if (!finalKeyword.trim()) {
        alert("Enter a keyword first");
        return;
      }

      setLoading(true);

      const res = await fetch("http://localhost:8000/blog/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          keyword: finalKeyword,
          secondary_keywords: [],
          target_location: "India",
          word_count: 1200,
          tone: "professional",
          competitor_urls: [],
          internal_links: [],
          enable_humanization: true,

          // 🔥 THIS IS THE MAGIC
          serp_analysis: overrideData.serpData || serpData,
        }),
      });

      const data = await res.json();
      console.log("BLOG DATA:", data);

      setBlogData(data);

      // 🔥 auto navigate to blog page
      handleNavigate("blog-gen");
    } catch (err) {
      console.error(err);
      alert("Error generating blog");
    } finally {
      setLoading(false);
    }
  };

  // 🔥 SERP ANALYSIS (global so Blog + Serp can share)
  const runSerpAnalysis = async (inputKeyword) => {
    try {
      const finalKeyword = inputKeyword || keyword;

      if (!finalKeyword.trim()) {
        alert("Enter keyword first");
        return;
      }

      setLoading(true);

      const res = await fetch("http://localhost:8000/serp/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          keyword: finalKeyword,
          target_location: "India",
        }),
      });

      const data = await res.json();
      console.log("SERP DATA:", data);

      setSerpData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ActivePage
      activePage={currentPage}
      onNavigate={handleNavigate}
      onLogout={handleLogout}
      authUser={authUser}
      // 🔥 SHARED STATE
      keyword={keyword}
      setKeyword={setKeyword}
      blogData={blogData}
      serpData={serpData}
      loading={loading}
      // 🔥 ACTIONS
      generateBlog={generateBlog}
      runSerpAnalysis={runSerpAnalysis}
      setSerpData={setSerpData}
    />
  );
}

export default function App() {
  return (
    <WorkflowProvider>
      <RouterShell />
    </WorkflowProvider>
  );
}
